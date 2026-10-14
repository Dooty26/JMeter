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

    var data = {"OkPercent": 43.54982206405694, "KoPercent": 56.45017793594306};
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
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.2778024911032028, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [0.177, 500, 1500, "HTTP Request - Chuyen Muc Thoi Su"], "isController": false}, {"data": [0.24, 500, 1500, "HTTP Request - Trang Chu VnExpress"], "isController": false}, {"data": [0.014, 500, 1500, "HTTP Request - Chuyen Muc So Hoa"], "isController": false}, {"data": [0.22945205479452055, 500, 1500, "HTTP Request - Chuyen Muc So Hoa-2"], "isController": false}, {"data": [0.9983388704318937, 500, 1500, "HTTP Request - Chuyen Muc So Hoa-0"], "isController": false}, {"data": [0.24916943521594684, 500, 1500, "HTTP Request - Chuyen Muc So Hoa-1"], "isController": false}]}, function(index, item){
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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 4496, 2538, 56.45017793594306, 368.20640569394993, 10, 1994, 240.0, 774.0, 1115.2999999999993, 1757.0299999999997, 208.16742290952865, 2960.7945288626265, 92.62060940249097], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["HTTP Request - Chuyen Muc Thoi Su", 1000, 646, 64.6, 269.7740000000003, 15, 854, 28.0, 739.0, 746.0, 788.8900000000001, 51.35579293344289, 1116.5962062512838, 19.057813783894822], "isController": false}, {"data": ["HTTP Request - Trang Chu VnExpress", 1000, 510, 51.0, 428.1999999999999, 34, 1886, 337.5, 780.0, 993.4499999999979, 1590.2900000000006, 49.28050463236743, 1287.7265363197318, 17.950808816282276], "isController": false}, {"data": ["HTTP Request - Chuyen Muc So Hoa", 1000, 890, 89.0, 482.598, 10, 1994, 294.5, 1259.9999999999995, 1748.8999999999999, 1813.0, 49.60809604127393, 415.92997352167873, 35.032617323147136], "isController": false}, {"data": ["HTTP Request - Chuyen Muc So Hoa-2", 292, 182, 62.32876712328767, 246.82191780821907, 16, 859, 29.5, 700.0, 723.4499999999998, 792.9699999999996, 15.140516436793527, 299.2687579396972, 5.781193287877216], "isController": false}, {"data": ["HTTP Request - Chuyen Muc So Hoa-0", 602, 0, 0.0, 303.9900332225916, 17, 561, 338.0, 399.70000000000005, 423.0, 456.85000000000014, 30.67515923566879, 44.623208598726116, 11.353403662420382], "isController": false}, {"data": ["HTTP Request - Chuyen Muc So Hoa-1", 602, 310, 51.49501661129568, 365.13289036544853, 15, 947, 57.0, 755.0, 761.0, 820.890000000001, 30.164854437039637, 52.241714216816156, 11.25290468256752], "isController": false}]}, function(index, item){
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
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["429/Too Many Requests", 2538, 100.0, 56.45017793594306], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 4496, 2538, "429/Too Many Requests", 2538, "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": ["HTTP Request - Chuyen Muc Thoi Su", 1000, 646, "429/Too Many Requests", 646, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["HTTP Request - Trang Chu VnExpress", 1000, 510, "429/Too Many Requests", 510, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["HTTP Request - Chuyen Muc So Hoa", 1000, 890, "429/Too Many Requests", 890, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["HTTP Request - Chuyen Muc So Hoa-2", 292, 182, "429/Too Many Requests", 182, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": ["HTTP Request - Chuyen Muc So Hoa-1", 602, 310, "429/Too Many Requests", 310, "", "", "", "", "", "", "", ""], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
