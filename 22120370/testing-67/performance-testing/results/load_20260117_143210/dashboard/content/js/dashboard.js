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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 1000, 0, 0.0, 33.621000000000016, 22, 62, 27.0, 52.0, 53.0, 55.0, 15.129279694993722, 44.847809493055664, 4.012509550357808], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["03 - Navigate to Timesheet-0", 100, 0, 0.0, 23.87, 23, 28, 24.0, 25.0, 25.0, 27.97999999999999, 1.589850395077823, 1.0837066169573444, 0.3151754201179669], "isController": false}, {"data": ["04 - View My Timesheet", 100, 0, 0.0, 51.45, 50, 56, 51.0, 53.0, 54.0, 55.989999999999995, 1.5893702914905115, 6.807471629740297, 0.5960138593089418], "isController": false}, {"data": ["02 - Submit Login-0", 100, 0, 0.0, 23.729999999999997, 22, 29, 23.0, 25.0, 25.94999999999999, 28.989999999999995, 1.5897240239094492, 1.0836204772351519, 0.5075007650546864], "isController": false}, {"data": ["01 - Get Login Page", 100, 0, 0.0, 28.68, 27, 62, 28.0, 30.0, 31.0, 61.70999999999985, 1.5887137773258768, 5.854425784228838, 0.21720696174377224], "isController": false}, {"data": ["02 - Submit Login-1", 100, 0, 0.0, 27.300000000000008, 26, 31, 27.0, 28.0, 29.0, 30.989999999999995, 1.5897240239094492, 5.931223074049345, 0.29031093014752635], "isController": false}, {"data": ["04 - View My Timesheet-0", 100, 0, 0.0, 23.919999999999995, 23, 27, 24.0, 25.0, 25.0, 26.989999999999995, 1.5900526307420775, 1.083844469001924, 0.30589879712518486], "isController": false}, {"data": ["04 - View My Timesheet-1", 100, 0, 0.0, 27.360000000000007, 26, 30, 27.0, 28.0, 29.0, 30.0, 1.5899767863389194, 5.726276552612332, 0.2903570889115019], "isController": false}, {"data": ["03 - Navigate to Timesheet-1", 100, 0, 0.0, 27.33, 26, 33, 27.0, 28.0, 29.0, 32.97999999999999, 1.5899009491708667, 5.726251848259854, 0.2903432397411641], "isController": false}, {"data": ["02 - Submit Login", 100, 0, 0.0, 51.19999999999998, 49, 60, 51.0, 53.0, 54.94999999999999, 59.95999999999998, 1.5890419665983377, 7.011833893470627, 0.7974694010106307], "isController": false}, {"data": ["03 - Navigate to Timesheet", 100, 0, 0.0, 51.37, 49, 58, 51.0, 53.900000000000006, 54.0, 58.0, 1.589168229348759, 6.806854479865239, 0.6052496185996249], "isController": false}]}, function(index, item){
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
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 1000, 0, "", "", "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
