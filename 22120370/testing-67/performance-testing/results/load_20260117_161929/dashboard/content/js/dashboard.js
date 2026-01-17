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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 1000, 0, 0.0, 33.37399999999997, 22, 66, 27.0, 51.0, 52.0, 54.0, 15.129279694993722, 44.85354207169009, 4.012509550357808], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["03 - Navigate to Timesheet-0", 100, 0, 0.0, 23.630000000000003, 22, 31, 23.0, 24.0, 25.0, 30.97999999999999, 1.5895218718209563, 1.0834826821592065, 0.315110292948881], "isController": false}, {"data": ["04 - View My Timesheet", 100, 0, 0.0, 51.16000000000002, 49, 57, 51.0, 53.0, 53.94999999999999, 56.989999999999995, 1.5888904777793669, 6.808349147758871, 0.5958339291672625], "isController": false}, {"data": ["02 - Submit Login-0", 100, 0, 0.0, 23.32, 22, 26, 23.0, 24.0, 24.94999999999999, 26.0, 1.5893955528712431, 1.0833965780313746, 0.5073959045250092], "isController": false}, {"data": ["01 - Get Login Page", 100, 0, 0.0, 28.06, 27, 48, 28.0, 29.0, 29.0, 47.82999999999991, 1.5886632987004734, 5.856442799185016, 0.21720006036920536], "isController": false}, {"data": ["02 - Submit Login-1", 100, 0, 0.0, 27.300000000000004, 26, 30, 27.0, 28.0, 28.0, 29.989999999999995, 1.5893702914905115, 5.9300119550446615, 0.2902463325280524], "isController": false}, {"data": ["04 - View My Timesheet-0", 100, 0, 0.0, 23.6, 23, 28, 23.0, 24.0, 25.0, 27.97999999999999, 1.5895724050230489, 1.0835171276426643, 0.3058064099507233], "isController": false}, {"data": ["04 - View My Timesheet-1", 100, 0, 0.0, 27.409999999999997, 26, 32, 27.0, 28.0, 29.0, 31.97999999999999, 1.589496606424745, 5.7274809310079, 0.2902693998060814], "isController": false}, {"data": ["03 - Navigate to Timesheet-1", 100, 0, 0.0, 27.31999999999999, 26, 37, 27.0, 28.0, 29.0, 36.93999999999997, 1.589420815054994, 5.7233894945244455, 0.29025555899930067], "isController": false}, {"data": ["02 - Submit Login", 100, 0, 0.0, 50.82000000000001, 49, 55, 51.0, 52.0, 53.0, 55.0, 1.5887137773258768, 7.010494323327084, 0.7973046974294611], "isController": false}, {"data": ["03 - Navigate to Timesheet", 100, 0, 0.0, 51.11999999999999, 49, 66, 51.0, 52.0, 53.94999999999999, 65.93999999999997, 1.5888147442008262, 6.8042077524229425, 0.6051149904671116], "isController": false}]}, function(index, item){
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
