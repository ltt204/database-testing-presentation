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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 1000, 0, 0.0, 117.36899999999993, 23, 357, 108.0, 233.0, 283.94999999999993, 318.0, 301.9323671497585, 895.4435339296498, 80.07694557669083], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["03 - Navigate to Timesheet-0", 100, 0, 0.0, 93.46, 28, 167, 85.5, 150.8, 158.95, 166.96999999999997, 45.662100456621005, 31.12514269406393, 9.052154680365296], "isController": false}, {"data": ["04 - View My Timesheet", 100, 0, 0.0, 170.39999999999995, 51, 327, 160.0, 302.1, 323.5999999999999, 326.99, 45.16711833785005, 193.52478192750678, 16.937669376693766], "isController": false}, {"data": ["02 - Submit Login-0", 100, 0, 0.0, 87.21999999999998, 24, 167, 92.0, 152.9, 156.0, 166.93999999999997, 47.551117451260104, 32.41277341892534, 15.180137006657155], "isController": false}, {"data": ["01 - Get Login Page", 100, 0, 0.0, 79.02, 28, 170, 60.0, 159.9, 161.95, 169.98, 48.92367906066536, 180.3754892367906, 6.688784246575342], "isController": false}, {"data": ["02 - Submit Login-1", 100, 0, 0.0, 95.79, 28, 169, 98.5, 158.9, 163.89999999999998, 168.96999999999997, 46.06172270842929, 171.97081198180564, 8.41166225241824], "isController": false}, {"data": ["04 - View My Timesheet-0", 100, 0, 0.0, 83.31999999999998, 23, 169, 81.5, 152.8, 158.89999999999998, 169.0, 45.72473708276177, 31.167838363054415, 8.796653520804757], "isController": false}, {"data": ["04 - View My Timesheet-1", 100, 0, 0.0, 86.88999999999997, 27, 172, 86.0, 149.0, 159.89999999999998, 172.0, 46.27487274409996, 166.7282761163813, 8.450587112447941], "isController": false}, {"data": ["03 - Navigate to Timesheet-1", 100, 0, 0.0, 100.35, 48, 198, 93.0, 156.9, 164.95, 197.7899999999999, 45.24886877828054, 163.0634014423077, 8.263221153846153], "isController": false}, {"data": ["02 - Submit Login", 100, 0, 0.0, 183.23999999999998, 53, 319, 199.0, 304.0, 309.9, 318.99, 45.47521600727603, 200.7788518929059, 22.82198584583902], "isController": false}, {"data": ["03 - Navigate to Timesheet", 100, 0, 0.0, 194.00000000000003, 76, 357, 178.0, 306.0, 316.0, 356.7499999999999, 44.58314757021846, 191.05402571890326, 16.97990971912617], "isController": false}]}, function(index, item){
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
