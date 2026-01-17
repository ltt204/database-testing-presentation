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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 2000, 0, 0.0, 33.23599999999998, 22, 64, 27.0, 51.0, 52.0, 54.0, 6.665111473989403, 19.761866762338787, 1.7676864981504317], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["03 - Navigate to Timesheet-0", 200, 0, 0.0, 23.505000000000006, 22, 32, 23.0, 24.0, 25.0, 28.970000000000027, 0.6702727339754546, 0.4568851253074876, 0.13287633300489968], "isController": false}, {"data": ["04 - View My Timesheet", 200, 0, 0.0, 50.92000000000001, 49, 64, 50.0, 52.0, 54.0, 57.99000000000001, 0.6702165804879847, 2.8715377030337352, 0.25133121768299427], "isController": false}, {"data": ["02 - Submit Login-0", 200, 0, 0.0, 23.205, 22, 27, 23.0, 24.0, 24.0, 26.980000000000018, 0.6702659950601396, 0.4568805317890405, 0.21397456424331995], "isController": false}, {"data": ["01 - Get Login Page", 200, 0, 0.0, 28.18999999999999, 26, 48, 28.0, 29.0, 30.0, 39.99000000000001, 0.6702053509195217, 2.470158321353413, 0.09162963782102837], "isController": false}, {"data": ["02 - Submit Login-1", 200, 0, 0.0, 27.254999999999995, 26, 30, 27.0, 28.0, 29.0, 29.99000000000001, 0.6702615025252102, 2.501034323463174, 0.12240127048067803], "isController": false}, {"data": ["04 - View My Timesheet-0", 200, 0, 0.0, 23.590000000000003, 22, 30, 23.0, 24.900000000000006, 25.0, 27.0, 0.6702794730262783, 0.456889718918303, 0.1289502501818133], "isController": false}, {"data": ["04 - View My Timesheet-1", 200, 0, 0.0, 27.195000000000007, 26, 40, 27.0, 28.0, 29.0, 31.99000000000001, 0.6702704876552933, 2.41488507374651, 0.12240291131986313], "isController": false}, {"data": ["03 - Navigate to Timesheet-1", 200, 0, 0.0, 27.159999999999993, 26, 30, 27.0, 28.0, 28.94999999999999, 30.0, 0.6702659950601396, 2.414845978110788, 0.12240209089477158], "isController": false}, {"data": ["02 - Submit Login", 200, 0, 0.0, 50.575000000000024, 49, 56, 50.0, 52.0, 53.0, 54.0, 0.6702031050509857, 2.957654080741044, 0.33634509344306796], "isController": false}, {"data": ["03 - Navigate to Timesheet", 200, 0, 0.0, 50.76500000000001, 49, 61, 50.5, 52.0, 53.0, 57.97000000000003, 0.6702120886154423, 2.871495550001173, 0.255256557187522], "isController": false}]}, function(index, item){
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
