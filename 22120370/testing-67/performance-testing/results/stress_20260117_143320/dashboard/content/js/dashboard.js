/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
var showControllersOnly = false;
var seriesFilter = "";
var filtersOnlySampleSeries = true;

/*
 * Add header in statistics table to group metrics by category
 * format
 *
 */
function summaryTableHeader(header) {
    var newRow = header.insertRow(-1);
    newRow.className = "tablesorter-no-sort";
    var cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Requests";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 3;
    cell.innerHTML = "Executions";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 7;
    cell.innerHTML = "Response Times (ms)";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Throughput";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 2;
    cell.innerHTML = "Network (KB/sec)";
    newRow.appendChild(cell);
}

/*
 * Populates the table identified by id parameter with the specified data and
 * format
 *
 */
function createTable(table, info, formatter, defaultSorts, seriesIndex, headerCreator) {
    var tableRef = table[0];

    // Create header and populate it with data.titles array
    var header = tableRef.createTHead();

    // Call callback is available
    if(headerCreator) {
        headerCreator(header);
    }

    var newRow = header.insertRow(-1);
    for (var index = 0; index < info.titles.length; index++) {
        var cell = document.createElement('th');
        cell.innerHTML = info.titles[index];
        newRow.appendChild(cell);
    }

    var tBody;

    // Create overall body if defined
    if(info.overall){
        tBody = document.createElement('tbody');
        tBody.className = "tablesorter-no-sort";
        tableRef.appendChild(tBody);
        var newRow = tBody.insertRow(-1);
        var data = info.overall.data;
        for(var index=0;index < data.length; index++){
            var cell = newRow.insertCell(-1);
            cell.innerHTML = formatter ? formatter(index, data[index]): data[index];
        }
    }

    // Create regular body
    tBody = document.createElement('tbody');
    tableRef.appendChild(tBody);

    var regexp;
    if(seriesFilter) {
        regexp = new RegExp(seriesFilter, 'i');
    }
    // Populate body with data.items array
    for(var index=0; index < info.items.length; index++){
        var item = info.items[index];
        if((!regexp || filtersOnlySampleSeries && !info.supportsControllersDiscrimination || regexp.test(item.data[seriesIndex]))
                &&
                (!showControllersOnly || !info.supportsControllersDiscrimination || item.isController)){
            if(item.data.length > 0) {
                var newRow = tBody.insertRow(-1);
                for(var col=0; col < item.data.length; col++){
                    var cell = newRow.insertCell(-1);
                    cell.innerHTML = formatter ? formatter(col, item.data[col]) : item.data[col];
                }
            }
        }
    }

    // Add support of columns sort
    table.tablesorter({sortList : defaultSorts});
}

$(document).ready(function() {

    // Customize table sorter default options
    $.extend( $.tablesorter.defaults, {
        theme: 'blue',
        cssInfoBlock: "tablesorter-no-sort",
        widthFixed: true,
        widgets: ['zebra']
    });

    var data = {"OkPercent": 100.0, "KoPercent": 0.0};
    var dataset = [
        {
            "label" : "FAIL",
            "data" : data.KoPercent,
            "color" : "#FF6347"
        },
        {
            "label" : "PASS",
            "data" : data.OkPercent,
            "color" : "#9ACD32"
        }];
    $.plot($("#flot-requests-summary"), dataset, {
        series : {
            pie : {
                show : true,
                radius : 1,
                label : {
                    show : true,
                    radius : 3 / 4,
                    formatter : function(label, series) {
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                            + label
                            + '<br/>'
                            + Math.round10(series.percent, -2)
                            + '%</div>';
                    },
                    background : {
                        opacity : 0.5,
                        color : '#000'
                    }
                }
            }
        },
        legend : {
            show : true
        }
    });

    // Creates APDEX table
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [1.0, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "03 - Navigate to Timesheet-0"], "isController": false}, {"data": [1.0, 500, 1500, "04 - View My Timesheet"], "isController": false}, {"data": [1.0, 500, 1500, "02 - Submit Login-0"], "isController": false}, {"data": [1.0, 500, 1500, "01 - Get Login Page"], "isController": false}, {"data": [1.0, 500, 1500, "02 - Submit Login-1"], "isController": false}, {"data": [1.0, 500, 1500, "04 - View My Timesheet-0"], "isController": false}, {"data": [1.0, 500, 1500, "04 - View My Timesheet-1"], "isController": false}, {"data": [1.0, 500, 1500, "03 - Navigate to Timesheet-1"], "isController": false}, {"data": [1.0, 500, 1500, "02 - Submit Login"], "isController": false}, {"data": [1.0, 500, 1500, "03 - Navigate to Timesheet"], "isController": false}]}, function(index, item){
        switch(index){
            case 0:
                item = item.toFixed(3);
                break;
            case 1:
            case 2:
                item = formatDuration(item);
                break;
        }
        return item;
    }, [[0, 0]], 3);

    // Create statistics table
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 2000, 0, 0.0, 33.23149999999995, 22, 58, 27.0, 51.0, 52.0, 54.0, 6.664933783882858, 19.759536999546786, 1.7676393720965884], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["03 - Navigate to Timesheet-0", 200, 0, 0.0, 23.564999999999998, 22, 27, 23.0, 24.0, 25.0, 26.0, 0.6702525176360195, 0.4568713450292398, 0.1328723252735468], "isController": false}, {"data": ["04 - View My Timesheet", 200, 0, 0.0, 50.94500000000001, 49, 58, 51.0, 52.0, 53.94999999999999, 56.0, 0.6701873843926761, 2.8705846955590033, 0.2513202691472536], "isController": false}, {"data": ["02 - Submit Login-0", 200, 0, 0.0, 23.21500000000001, 22, 27, 23.0, 24.0, 25.0, 26.99000000000001, 0.670245779127206, 0.45686675178788055, 0.21396811054363635], "isController": false}, {"data": ["01 - Get Login Page", 200, 0, 0.0, 27.985000000000014, 27, 44, 28.0, 29.0, 29.0, 33.98000000000002, 0.6701941217273584, 2.4705619849977047, 0.09162810257991227], "isController": false}, {"data": ["02 - Submit Login-1", 200, 0, 0.0, 27.275000000000013, 26, 34, 27.0, 28.0, 29.0, 32.0, 0.6702435329877111, 2.5003781901497657, 0.12239798893427926], "isController": false}, {"data": ["04 - View My Timesheet-0", 200, 0, 0.0, 23.664999999999992, 22, 28, 24.0, 24.0, 25.0, 27.99000000000001, 0.6702480252817555, 0.45686828285807163, 0.12894420017627523], "isController": false}, {"data": ["04 - View My Timesheet-1", 200, 0, 0.0, 27.165, 26, 33, 27.0, 28.0, 28.0, 30.99000000000001, 0.6702435329877111, 2.4139599736845634, 0.12239798893427926], "isController": false}, {"data": ["03 - Navigate to Timesheet-1", 200, 0, 0.0, 27.089999999999993, 26, 30, 27.0, 28.0, 28.0, 29.0, 0.6702412868632708, 2.4150449532925604, 0.12239757875335122], "isController": false}, {"data": ["02 - Submit Login", 200, 0, 0.0, 50.61000000000001, 49, 57, 50.0, 52.0, 54.0, 56.0, 0.6701828929114755, 2.956975855195258, 0.33633494987031964], "isController": false}, {"data": ["03 - Navigate to Timesheet", 200, 0, 0.0, 50.79999999999999, 49, 55, 51.0, 52.0, 53.0, 54.0, 0.6701873843926761, 2.871677676937847, 0.2552471483526794], "isController": false}]}, function(index, item){
        switch(index){
            // Errors pct
            case 3:
                item = item.toFixed(2) + '%';
                break;
            // Mean
            case 4:
            // Mean
            case 7:
            // Median
            case 8:
            // Percentile 1
            case 9:
            // Percentile 2
            case 10:
            // Percentile 3
            case 11:
            // Throughput
            case 12:
            // Kbytes/s
            case 13:
            // Sent Kbytes/s
                item = item.toFixed(2);
                break;
        }
        return item;
    }, [[0, 0]], 0, summaryTableHeader);

    // Create error table
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": []}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 2000, 0, "", "", "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
