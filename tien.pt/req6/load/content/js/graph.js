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
$(document).ready(function() {

    $(".click-title").mouseenter( function(    e){
        e.preventDefault();
        this.style.cursor="pointer";
    });
    $(".click-title").mousedown( function(event){
        event.preventDefault();
    });

    // Ugly code while this script is shared among several pages
    try{
        refreshHitsPerSecond(true);
    } catch(e){}
    try{
        refreshResponseTimeOverTime(true);
    } catch(e){}
    try{
        refreshResponseTimePercentiles();
    } catch(e){}
});


var responseTimePercentilesInfos = {
        data: {"result": {"minY": 39.0, "minX": 0.0, "maxY": 3791.0, "series": [{"data": [[0.0, 39.0], [0.1, 39.0], [0.2, 41.0], [0.3, 41.0], [0.4, 65.0], [0.5, 65.0], [0.6, 65.0], [0.7, 70.0], [0.8, 164.0], [0.9, 164.0], [1.0, 414.0], [1.1, 414.0], [1.2, 934.0], [1.3, 934.0], [1.4, 1599.0], [1.5, 1599.0], [1.6, 1599.0], [1.7, 1599.0], [1.8, 1628.0], [1.9, 1628.0], [2.0, 1629.0], [2.1, 1629.0], [2.2, 1630.0], [2.3, 1630.0], [2.4, 1633.0], [2.5, 1633.0], [2.6, 1676.0], [2.7, 1676.0], [2.8, 1676.0], [2.9, 1678.0], [3.0, 1678.0], [3.1, 1678.0], [3.2, 1717.0], [3.3, 1717.0], [3.4, 1717.0], [3.5, 1718.0], [3.6, 1718.0], [3.7, 1719.0], [3.8, 1719.0], [3.9, 1750.0], [4.0, 1750.0], [4.1, 1751.0], [4.2, 1751.0], [4.3, 1754.0], [4.4, 1754.0], [4.5, 1756.0], [4.6, 1756.0], [4.7, 1779.0], [4.8, 1779.0], [4.9, 1780.0], [5.0, 1780.0], [5.1, 1781.0], [5.2, 1781.0], [5.3, 1782.0], [5.4, 1782.0], [5.5, 1798.0], [5.6, 1798.0], [5.7, 1799.0], [5.8, 1799.0], [5.9, 1800.0], [6.0, 1800.0], [6.1, 1803.0], [6.2, 1803.0], [6.3, 1848.0], [6.4, 1848.0], [6.5, 1850.0], [6.6, 1850.0], [6.7, 1851.0], [6.8, 1851.0], [6.9, 1852.0], [7.0, 1852.0], [7.1, 1880.0], [7.2, 1880.0], [7.3, 1886.0], [7.4, 1886.0], [7.5, 1888.0], [7.6, 1888.0], [7.7, 1888.0], [7.8, 1888.0], [7.9, 1889.0], [8.0, 1889.0], [8.1, 1905.0], [8.2, 1905.0], [8.3, 1931.0], [8.4, 1931.0], [8.5, 1934.0], [8.6, 1934.0], [8.7, 1935.0], [8.8, 1969.0], [8.9, 1969.0], [9.0, 1970.0], [9.1, 1970.0], [9.2, 1971.0], [9.3, 1971.0], [9.4, 1973.0], [9.5, 1973.0], [9.6, 2002.0], [9.7, 2002.0], [9.8, 2004.0], [9.9, 2004.0], [10.0, 2004.0], [10.1, 2004.0], [10.2, 2004.0], [10.3, 2004.0], [10.4, 2035.0], [10.5, 2035.0], [10.6, 2036.0], [10.7, 2036.0], [10.8, 2036.0], [10.9, 2036.0], [11.0, 2038.0], [11.1, 2038.0], [11.2, 2070.0], [11.3, 2070.0], [11.4, 2071.0], [11.5, 2071.0], [11.6, 2072.0], [11.7, 2072.0], [11.8, 2072.0], [11.9, 2072.0], [12.0, 2102.0], [12.1, 2102.0], [12.2, 2104.0], [12.3, 2104.0], [12.4, 2104.0], [12.5, 2104.0], [12.6, 2104.0], [12.7, 2104.0], [12.8, 2130.0], [12.9, 2130.0], [13.0, 2131.0], [13.1, 2131.0], [13.2, 2141.0], [13.3, 2141.0], [13.4, 2148.0], [13.5, 2148.0], [13.6, 2170.0], [13.7, 2170.0], [13.8, 2182.0], [13.9, 2182.0], [14.0, 2182.0], [14.1, 2182.0], [14.2, 2185.0], [14.3, 2185.0], [14.4, 2186.0], [14.5, 2186.0], [14.6, 2198.0], [14.7, 2198.0], [14.8, 2215.0], [14.9, 2215.0], [15.0, 2217.0], [15.1, 2217.0], [15.2, 2219.0], [15.3, 2219.0], [15.4, 2219.0], [15.5, 2219.0], [15.6, 2232.0], [15.7, 2232.0], [15.8, 2246.0], [15.9, 2246.0], [16.0, 2253.0], [16.1, 2253.0], [16.2, 2257.0], [16.3, 2257.0], [16.4, 2258.0], [16.5, 2258.0], [16.6, 2259.0], [16.7, 2259.0], [16.8, 2288.0], [16.9, 2288.0], [17.0, 2295.0], [17.1, 2295.0], [17.2, 2296.0], [17.3, 2296.0], [17.4, 2297.0], [17.5, 2297.0], [17.6, 2302.0], [17.7, 2302.0], [17.8, 2304.0], [17.9, 2304.0], [18.0, 2338.0], [18.1, 2338.0], [18.2, 2339.0], [18.3, 2339.0], [18.4, 2339.0], [18.5, 2339.0], [18.6, 2339.0], [18.7, 2339.0], [18.8, 2372.0], [18.9, 2372.0], [19.0, 2375.0], [19.1, 2375.0], [19.2, 2376.0], [19.3, 2376.0], [19.4, 2377.0], [19.5, 2377.0], [19.6, 2409.0], [19.7, 2409.0], [19.8, 2410.0], [19.9, 2410.0], [20.0, 2411.0], [20.1, 2411.0], [20.2, 2411.0], [20.3, 2411.0], [20.4, 2424.0], [20.5, 2424.0], [20.6, 2437.0], [20.7, 2437.0], [20.8, 2441.0], [20.9, 2441.0], [21.0, 2442.0], [21.1, 2442.0], [21.2, 2445.0], [21.3, 2445.0], [21.4, 2452.0], [21.5, 2452.0], [21.6, 2460.0], [21.7, 2460.0], [21.8, 2460.0], [21.9, 2460.0], [22.0, 2461.0], [22.1, 2461.0], [22.2, 2466.0], [22.3, 2466.0], [22.4, 2477.0], [22.5, 2477.0], [22.6, 2507.0], [22.7, 2507.0], [22.8, 2507.0], [22.9, 2507.0], [23.0, 2519.0], [23.1, 2519.0], [23.2, 2520.0], [23.3, 2520.0], [23.4, 2520.0], [23.5, 2520.0], [23.6, 2520.0], [23.7, 2520.0], [23.8, 2521.0], [23.9, 2521.0], [24.0, 2521.0], [24.1, 2521.0], [24.2, 2522.0], [24.3, 2522.0], [24.4, 2522.0], [24.5, 2522.0], [24.6, 2522.0], [24.7, 2522.0], [24.8, 2523.0], [24.9, 2523.0], [25.0, 2525.0], [25.1, 2525.0], [25.2, 2525.0], [25.3, 2525.0], [25.4, 2528.0], [25.5, 2528.0], [25.6, 2530.0], [25.7, 2530.0], [25.8, 2530.0], [25.9, 2530.0], [26.0, 2530.0], [26.1, 2530.0], [26.2, 2533.0], [26.3, 2533.0], [26.4, 2536.0], [26.5, 2536.0], [26.6, 2538.0], [26.7, 2538.0], [26.8, 2540.0], [26.9, 2540.0], [27.0, 2542.0], [27.1, 2542.0], [27.2, 2545.0], [27.3, 2545.0], [27.4, 2552.0], [27.5, 2552.0], [27.6, 2552.0], [27.7, 2552.0], [27.8, 2555.0], [27.9, 2555.0], [28.0, 2555.0], [28.1, 2555.0], [28.2, 2555.0], [28.3, 2555.0], [28.4, 2556.0], [28.5, 2556.0], [28.6, 2557.0], [28.7, 2557.0], [28.8, 2557.0], [28.9, 2557.0], [29.0, 2557.0], [29.1, 2557.0], [29.2, 2562.0], [29.3, 2562.0], [29.4, 2563.0], [29.5, 2563.0], [29.6, 2563.0], [29.7, 2563.0], [29.8, 2574.0], [29.9, 2574.0], [30.0, 2574.0], [30.1, 2574.0], [30.2, 2574.0], [30.3, 2574.0], [30.4, 2575.0], [30.5, 2575.0], [30.6, 2576.0], [30.7, 2576.0], [30.8, 2576.0], [30.9, 2576.0], [31.0, 2577.0], [31.1, 2577.0], [31.2, 2578.0], [31.3, 2578.0], [31.4, 2578.0], [31.5, 2578.0], [31.6, 2581.0], [31.7, 2581.0], [31.8, 2581.0], [31.9, 2581.0], [32.0, 2582.0], [32.1, 2582.0], [32.2, 2584.0], [32.3, 2584.0], [32.4, 2594.0], [32.5, 2594.0], [32.6, 2596.0], [32.7, 2596.0], [32.8, 2598.0], [32.9, 2598.0], [33.0, 2598.0], [33.1, 2598.0], [33.2, 2598.0], [33.3, 2598.0], [33.4, 2598.0], [33.5, 2598.0], [33.6, 2603.0], [33.7, 2603.0], [33.8, 2604.0], [33.9, 2604.0], [34.0, 2606.0], [34.1, 2606.0], [34.2, 2610.0], [34.3, 2610.0], [34.4, 2610.0], [34.5, 2610.0], [34.6, 2611.0], [34.7, 2611.0], [34.8, 2612.0], [34.9, 2612.0], [35.0, 2612.0], [35.1, 2612.0], [35.2, 2612.0], [35.3, 2612.0], [35.4, 2613.0], [35.5, 2613.0], [35.6, 2614.0], [35.7, 2614.0], [35.8, 2614.0], [35.9, 2614.0], [36.0, 2614.0], [36.1, 2614.0], [36.2, 2614.0], [36.3, 2614.0], [36.4, 2615.0], [36.5, 2615.0], [36.6, 2616.0], [36.7, 2616.0], [36.8, 2616.0], [36.9, 2616.0], [37.0, 2617.0], [37.1, 2617.0], [37.2, 2617.0], [37.3, 2617.0], [37.4, 2618.0], [37.5, 2618.0], [37.6, 2619.0], [37.7, 2619.0], [37.8, 2619.0], [37.9, 2619.0], [38.0, 2619.0], [38.1, 2619.0], [38.2, 2620.0], [38.3, 2620.0], [38.4, 2621.0], [38.5, 2621.0], [38.6, 2624.0], [38.7, 2624.0], [38.8, 2627.0], [38.9, 2627.0], [39.0, 2631.0], [39.1, 2631.0], [39.2, 2633.0], [39.3, 2633.0], [39.4, 2638.0], [39.5, 2638.0], [39.6, 2640.0], [39.7, 2640.0], [39.8, 2646.0], [39.9, 2646.0], [40.0, 2646.0], [40.1, 2646.0], [40.2, 2647.0], [40.3, 2647.0], [40.4, 2648.0], [40.5, 2648.0], [40.6, 2650.0], [40.7, 2650.0], [40.8, 2650.0], [40.9, 2650.0], [41.0, 2652.0], [41.1, 2652.0], [41.2, 2652.0], [41.3, 2652.0], [41.4, 2654.0], [41.5, 2654.0], [41.6, 2654.0], [41.7, 2654.0], [41.8, 2655.0], [41.9, 2655.0], [42.0, 2661.0], [42.1, 2661.0], [42.2, 2664.0], [42.3, 2664.0], [42.4, 2664.0], [42.5, 2665.0], [42.6, 2665.0], [42.7, 2667.0], [42.8, 2667.0], [42.9, 2670.0], [43.0, 2670.0], [43.1, 2671.0], [43.2, 2671.0], [43.3, 2671.0], [43.4, 2671.0], [43.5, 2673.0], [43.6, 2673.0], [43.7, 2676.0], [43.8, 2676.0], [43.9, 2678.0], [44.0, 2678.0], [44.1, 2690.0], [44.2, 2690.0], [44.3, 2690.0], [44.4, 2690.0], [44.5, 2691.0], [44.6, 2691.0], [44.7, 2693.0], [44.8, 2693.0], [44.9, 2693.0], [45.0, 2693.0], [45.1, 2694.0], [45.2, 2694.0], [45.3, 2695.0], [45.4, 2695.0], [45.5, 2696.0], [45.6, 2696.0], [45.7, 2703.0], [45.8, 2703.0], [45.9, 2703.0], [46.0, 2703.0], [46.1, 2703.0], [46.2, 2703.0], [46.3, 2703.0], [46.4, 2703.0], [46.5, 2703.0], [46.6, 2703.0], [46.7, 2703.0], [46.8, 2703.0], [46.9, 2704.0], [47.0, 2704.0], [47.1, 2704.0], [47.2, 2704.0], [47.3, 2704.0], [47.4, 2704.0], [47.5, 2705.0], [47.6, 2705.0], [47.7, 2705.0], [47.8, 2705.0], [47.9, 2705.0], [48.0, 2705.0], [48.1, 2705.0], [48.2, 2705.0], [48.3, 2705.0], [48.4, 2705.0], [48.5, 2706.0], [48.6, 2706.0], [48.7, 2706.0], [48.8, 2706.0], [48.9, 2706.0], [49.0, 2706.0], [49.1, 2707.0], [49.2, 2707.0], [49.3, 2707.0], [49.4, 2707.0], [49.5, 2707.0], [49.6, 2707.0], [49.7, 2707.0], [49.8, 2707.0], [49.9, 2708.0], [50.0, 2708.0], [50.1, 2711.0], [50.2, 2711.0], [50.3, 2712.0], [50.4, 2712.0], [50.5, 2713.0], [50.6, 2713.0], [50.7, 2714.0], [50.8, 2714.0], [50.9, 2718.0], [51.0, 2718.0], [51.1, 2724.0], [51.2, 2724.0], [51.3, 2727.0], [51.4, 2727.0], [51.5, 2728.0], [51.6, 2728.0], [51.7, 2728.0], [51.8, 2728.0], [51.9, 2728.0], [52.0, 2728.0], [52.1, 2728.0], [52.2, 2728.0], [52.3, 2730.0], [52.4, 2730.0], [52.5, 2730.0], [52.6, 2730.0], [52.7, 2731.0], [52.8, 2731.0], [52.9, 2733.0], [53.0, 2733.0], [53.1, 2735.0], [53.2, 2735.0], [53.3, 2735.0], [53.4, 2735.0], [53.5, 2736.0], [53.6, 2736.0], [53.7, 2736.0], [53.8, 2736.0], [53.9, 2737.0], [54.0, 2737.0], [54.1, 2738.0], [54.2, 2738.0], [54.3, 2739.0], [54.4, 2739.0], [54.5, 2740.0], [54.6, 2740.0], [54.7, 2741.0], [54.8, 2741.0], [54.9, 2741.0], [55.0, 2741.0], [55.1, 2742.0], [55.2, 2742.0], [55.3, 2744.0], [55.4, 2744.0], [55.5, 2744.0], [55.6, 2744.0], [55.7, 2744.0], [55.8, 2744.0], [55.9, 2762.0], [56.0, 2762.0], [56.1, 2763.0], [56.2, 2763.0], [56.3, 2763.0], [56.4, 2763.0], [56.5, 2763.0], [56.6, 2763.0], [56.7, 2767.0], [56.8, 2767.0], [56.9, 2769.0], [57.0, 2769.0], [57.1, 2769.0], [57.2, 2769.0], [57.3, 2770.0], [57.4, 2770.0], [57.5, 2770.0], [57.6, 2770.0], [57.7, 2770.0], [57.8, 2770.0], [57.9, 2773.0], [58.0, 2773.0], [58.1, 2774.0], [58.2, 2774.0], [58.3, 2776.0], [58.4, 2776.0], [58.5, 2781.0], [58.6, 2781.0], [58.7, 2783.0], [58.8, 2783.0], [58.9, 2789.0], [59.0, 2789.0], [59.1, 2790.0], [59.2, 2790.0], [59.3, 2793.0], [59.4, 2793.0], [59.5, 2793.0], [59.6, 2793.0], [59.7, 2793.0], [59.8, 2793.0], [59.9, 2794.0], [60.0, 2794.0], [60.1, 2795.0], [60.2, 2795.0], [60.3, 2798.0], [60.4, 2798.0], [60.5, 2799.0], [60.6, 2799.0], [60.7, 2801.0], [60.8, 2801.0], [60.9, 2806.0], [61.0, 2806.0], [61.1, 2806.0], [61.2, 2806.0], [61.3, 2806.0], [61.4, 2806.0], [61.5, 2807.0], [61.6, 2807.0], [61.7, 2809.0], [61.8, 2809.0], [61.9, 2809.0], [62.0, 2809.0], [62.1, 2825.0], [62.2, 2825.0], [62.3, 2825.0], [62.4, 2825.0], [62.5, 2849.0], [62.6, 2849.0], [62.7, 2862.0], [62.8, 2862.0], [62.9, 2864.0], [63.0, 2864.0], [63.1, 2891.0], [63.2, 2891.0], [63.3, 2901.0], [63.4, 2901.0], [63.5, 2906.0], [63.6, 2906.0], [63.7, 2912.0], [63.8, 2912.0], [63.9, 2922.0], [64.0, 2922.0], [64.1, 2926.0], [64.2, 2926.0], [64.3, 2954.0], [64.4, 2954.0], [64.5, 2963.0], [64.6, 2963.0], [64.7, 2974.0], [64.8, 2974.0], [64.9, 3007.0], [65.0, 3007.0], [65.1, 3009.0], [65.2, 3009.0], [65.3, 3018.0], [65.4, 3018.0], [65.5, 3025.0], [65.6, 3025.0], [65.7, 3033.0], [65.8, 3033.0], [65.9, 3037.0], [66.0, 3037.0], [66.1, 3068.0], [66.2, 3068.0], [66.3, 3070.0], [66.4, 3070.0], [66.5, 3071.0], [66.6, 3071.0], [66.7, 3071.0], [66.8, 3071.0], [66.9, 3073.0], [67.0, 3073.0], [67.1, 3074.0], [67.2, 3074.0], [67.3, 3075.0], [67.4, 3075.0], [67.5, 3079.0], [67.6, 3079.0], [67.7, 3082.0], [67.8, 3082.0], [67.9, 3085.0], [68.0, 3085.0], [68.1, 3093.0], [68.2, 3093.0], [68.3, 3094.0], [68.4, 3094.0], [68.5, 3097.0], [68.6, 3097.0], [68.7, 3097.0], [68.8, 3097.0], [68.9, 3098.0], [69.0, 3098.0], [69.1, 3099.0], [69.2, 3099.0], [69.3, 3099.0], [69.4, 3099.0], [69.5, 3100.0], [69.6, 3100.0], [69.7, 3100.0], [69.8, 3100.0], [69.9, 3101.0], [70.0, 3101.0], [70.1, 3103.0], [70.2, 3103.0], [70.3, 3104.0], [70.4, 3104.0], [70.5, 3104.0], [70.6, 3104.0], [70.7, 3130.0], [70.8, 3130.0], [70.9, 3131.0], [71.0, 3131.0], [71.1, 3169.0], [71.2, 3169.0], [71.3, 3172.0], [71.4, 3172.0], [71.5, 3172.0], [71.6, 3172.0], [71.7, 3177.0], [71.8, 3177.0], [71.9, 3187.0], [72.0, 3187.0], [72.1, 3187.0], [72.2, 3187.0], [72.3, 3190.0], [72.4, 3190.0], [72.5, 3192.0], [72.6, 3192.0], [72.7, 3194.0], [72.8, 3194.0], [72.9, 3208.0], [73.0, 3208.0], [73.1, 3210.0], [73.2, 3210.0], [73.3, 3211.0], [73.4, 3211.0], [73.5, 3213.0], [73.6, 3213.0], [73.7, 3214.0], [73.8, 3214.0], [73.9, 3228.0], [74.0, 3228.0], [74.1, 3234.0], [74.2, 3234.0], [74.3, 3234.0], [74.4, 3234.0], [74.5, 3235.0], [74.6, 3235.0], [74.7, 3236.0], [74.8, 3236.0], [74.9, 3246.0], [75.0, 3246.0], [75.1, 3247.0], [75.2, 3247.0], [75.3, 3251.0], [75.4, 3251.0], [75.5, 3252.0], [75.6, 3252.0], [75.7, 3254.0], [75.8, 3254.0], [75.9, 3266.0], [76.0, 3266.0], [76.1, 3267.0], [76.2, 3267.0], [76.3, 3268.0], [76.4, 3268.0], [76.5, 3269.0], [76.6, 3269.0], [76.7, 3275.0], [76.8, 3275.0], [76.9, 3280.0], [77.0, 3280.0], [77.1, 3282.0], [77.2, 3282.0], [77.3, 3282.0], [77.4, 3282.0], [77.5, 3282.0], [77.6, 3282.0], [77.7, 3286.0], [77.8, 3286.0], [77.9, 3289.0], [78.0, 3289.0], [78.1, 3298.0], [78.2, 3298.0], [78.3, 3300.0], [78.4, 3300.0], [78.5, 3303.0], [78.6, 3303.0], [78.7, 3306.0], [78.8, 3306.0], [78.9, 3313.0], [79.0, 3313.0], [79.1, 3314.0], [79.2, 3314.0], [79.3, 3326.0], [79.4, 3326.0], [79.5, 3350.0], [79.6, 3350.0], [79.7, 3375.0], [79.8, 3375.0], [79.9, 3395.0], [80.0, 3395.0], [80.1, 3413.0], [80.2, 3413.0], [80.3, 3440.0], [80.4, 3440.0], [80.5, 3443.0], [80.6, 3443.0], [80.7, 3448.0], [80.8, 3448.0], [80.9, 3449.0], [81.0, 3449.0], [81.1, 3471.0], [81.2, 3471.0], [81.3, 3482.0], [81.4, 3482.0], [81.5, 3484.0], [81.6, 3484.0], [81.7, 3489.0], [81.8, 3489.0], [81.9, 3490.0], [82.0, 3490.0], [82.1, 3490.0], [82.2, 3490.0], [82.3, 3506.0], [82.4, 3506.0], [82.5, 3507.0], [82.6, 3507.0], [82.7, 3508.0], [82.8, 3508.0], [82.9, 3509.0], [83.0, 3509.0], [83.1, 3513.0], [83.2, 3513.0], [83.3, 3514.0], [83.4, 3514.0], [83.5, 3520.0], [83.6, 3520.0], [83.7, 3528.0], [83.8, 3528.0], [83.9, 3538.0], [84.0, 3538.0], [84.1, 3554.0], [84.2, 3554.0], [84.3, 3555.0], [84.4, 3555.0], [84.5, 3556.0], [84.6, 3556.0], [84.7, 3600.0], [84.8, 3600.0], [84.9, 3628.0], [85.0, 3628.0], [85.1, 3635.0], [85.2, 3635.0], [85.3, 3639.0], [85.4, 3639.0], [85.5, 3648.0], [85.6, 3648.0], [85.7, 3651.0], [85.8, 3651.0], [85.9, 3652.0], [86.0, 3652.0], [86.1, 3658.0], [86.2, 3658.0], [86.3, 3659.0], [86.4, 3659.0], [86.5, 3660.0], [86.6, 3660.0], [86.7, 3661.0], [86.8, 3661.0], [86.9, 3666.0], [87.0, 3666.0], [87.1, 3670.0], [87.2, 3670.0], [87.3, 3671.0], [87.4, 3671.0], [87.5, 3674.0], [87.6, 3674.0], [87.7, 3676.0], [87.8, 3676.0], [87.9, 3678.0], [88.0, 3678.0], [88.1, 3682.0], [88.2, 3682.0], [88.3, 3685.0], [88.4, 3685.0], [88.5, 3686.0], [88.6, 3686.0], [88.7, 3689.0], [88.8, 3689.0], [88.9, 3689.0], [89.0, 3689.0], [89.1, 3694.0], [89.2, 3694.0], [89.3, 3694.0], [89.4, 3694.0], [89.5, 3696.0], [89.6, 3696.0], [89.7, 3697.0], [89.8, 3697.0], [89.9, 3697.0], [90.0, 3697.0], [90.1, 3699.0], [90.2, 3699.0], [90.3, 3701.0], [90.4, 3701.0], [90.5, 3704.0], [90.6, 3704.0], [90.7, 3707.0], [90.8, 3707.0], [90.9, 3709.0], [91.0, 3709.0], [91.1, 3715.0], [91.2, 3715.0], [91.3, 3719.0], [91.4, 3719.0], [91.5, 3720.0], [91.6, 3720.0], [91.7, 3723.0], [91.8, 3723.0], [91.9, 3723.0], [92.0, 3723.0], [92.1, 3724.0], [92.2, 3724.0], [92.3, 3725.0], [92.4, 3725.0], [92.5, 3728.0], [92.6, 3728.0], [92.7, 3729.0], [92.8, 3729.0], [92.9, 3729.0], [93.0, 3729.0], [93.1, 3729.0], [93.2, 3729.0], [93.3, 3731.0], [93.4, 3731.0], [93.5, 3740.0], [93.6, 3740.0], [93.7, 3740.0], [93.8, 3740.0], [93.9, 3741.0], [94.0, 3741.0], [94.1, 3743.0], [94.2, 3743.0], [94.3, 3743.0], [94.4, 3743.0], [94.5, 3744.0], [94.6, 3744.0], [94.7, 3746.0], [94.8, 3746.0], [94.9, 3748.0], [95.0, 3748.0], [95.1, 3749.0], [95.2, 3749.0], [95.3, 3751.0], [95.4, 3751.0], [95.5, 3754.0], [95.6, 3754.0], [95.7, 3754.0], [95.8, 3754.0], [95.9, 3754.0], [96.0, 3754.0], [96.1, 3755.0], [96.2, 3755.0], [96.3, 3758.0], [96.4, 3758.0], [96.5, 3763.0], [96.6, 3763.0], [96.7, 3767.0], [96.8, 3767.0], [96.9, 3767.0], [97.0, 3767.0], [97.1, 3768.0], [97.2, 3768.0], [97.3, 3770.0], [97.4, 3770.0], [97.5, 3770.0], [97.6, 3770.0], [97.7, 3770.0], [97.8, 3770.0], [97.9, 3771.0], [98.0, 3771.0], [98.1, 3772.0], [98.2, 3772.0], [98.3, 3772.0], [98.4, 3772.0], [98.5, 3773.0], [98.6, 3773.0], [98.7, 3773.0], [98.8, 3773.0], [98.9, 3775.0], [99.0, 3775.0], [99.1, 3777.0], [99.2, 3777.0], [99.3, 3778.0], [99.4, 3778.0], [99.5, 3779.0], [99.6, 3779.0], [99.7, 3782.0], [99.8, 3782.0], [99.9, 3791.0], [100.0, 3791.0]], "isOverall": false, "label": "Create Candidate Request", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 100.0, "title": "Response Time Percentiles"}},
        getOptions: function() {
            return {
                series: {
                    points: { show: false }
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentiles'
                },
                xaxis: {
                    tickDecimals: 1,
                    axisLabel: "Percentiles",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Percentile value in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : %x.2 percentile was %y ms"
                },
                selection: { mode: "xy" },
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentiles"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesPercentiles"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesPercentiles"), dataset, prepareOverviewOptions(options));
        }
};

/**
 * @param elementId Id of element where we display message
 */
function setEmptyGraph(elementId) {
    $(function() {
        $(elementId).text("No graph series with filter="+seriesFilter);
    });
}

// Response times percentiles
function refreshResponseTimePercentiles() {
    var infos = responseTimePercentilesInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimePercentiles");
        return;
    }
    if (isGraph($("#flotResponseTimesPercentiles"))){
        infos.createGraph();
    } else {
        var choiceContainer = $("#choicesResponseTimePercentiles");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesPercentiles", "#overviewResponseTimesPercentiles");
        $('#bodyResponseTimePercentiles .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimeDistributionInfos = {
        data: {"result": {"minY": 1.0, "minX": 0.0, "maxY": 75.0, "series": [{"data": [[0.0, 4.0], [900.0, 1.0], [1500.0, 2.0], [100.0, 1.0], [1600.0, 7.0], [1700.0, 13.0], [1800.0, 11.0], [1900.0, 8.0], [2000.0, 12.0], [2100.0, 14.0], [2200.0, 14.0], [2300.0, 10.0], [2400.0, 15.0], [2500.0, 55.0], [2600.0, 60.0], [2700.0, 75.0], [2800.0, 13.0], [2900.0, 8.0], [3000.0, 23.0], [3100.0, 17.0], [3200.0, 27.0], [3300.0, 9.0], [3400.0, 11.0], [3500.0, 12.0], [3600.0, 28.0], [3700.0, 49.0], [400.0, 1.0]], "isOverall": false, "label": "Create Candidate Request", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 100, "maxX": 3700.0, "title": "Response Time Distribution"}},
        getOptions: function() {
            var granularity = this.data.result.granularity;
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    barWidth: this.data.result.granularity
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " responses for " + label + " were between " + xval + " and " + (xval + granularity) + " ms";
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimeDistribution"), prepareData(data.result.series, $("#choicesResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshResponseTimeDistribution() {
    var infos = responseTimeDistributionInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeDistribution");
        return;
    }
    if (isGraph($("#flotResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var syntheticResponseTimeDistributionInfos = {
        data: {"result": {"minY": 1.0, "minX": 0.0, "ticks": [[0, "Requests having \nresponse time <= 500ms"], [1, "Requests having \nresponse time > 500ms and <= 1,500ms"], [2, "Requests having \nresponse time > 1,500ms"], [3, "Requests in error"]], "maxY": 493.0, "series": [{"data": [[0.0, 6.0]], "color": "#9ACD32", "isOverall": false, "label": "Requests having \nresponse time <= 500ms", "isController": false}, {"data": [[1.0, 1.0]], "color": "yellow", "isOverall": false, "label": "Requests having \nresponse time > 500ms and <= 1,500ms", "isController": false}, {"data": [[2.0, 493.0]], "color": "orange", "isOverall": false, "label": "Requests having \nresponse time > 1,500ms", "isController": false}, {"data": [], "color": "#FF6347", "isOverall": false, "label": "Requests in error", "isController": false}], "supportsControllersDiscrimination": false, "maxX": 2.0, "title": "Synthetic Response Times Distribution"}},
        getOptions: function() {
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendSyntheticResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times ranges",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                    tickLength:0,
                    min:-0.5,
                    max:3.5
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    align: "center",
                    barWidth: 0.25,
                    fill:.75
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " " + label;
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            options.xaxis.ticks = data.result.ticks;
            $.plot($("#flotSyntheticResponseTimeDistribution"), prepareData(data.result.series, $("#choicesSyntheticResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshSyntheticResponseTimeDistribution() {
    var infos = syntheticResponseTimeDistributionInfos;
    prepareSeries(infos.data, true);
    if (isGraph($("#flotSyntheticResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerSyntheticResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var activeThreadsOverTimeInfos = {
        data: {"result": {"minY": 88.07799999999995, "minX": 1.7683236E12, "maxY": 88.07799999999995, "series": [{"data": [[1.7683236E12, 88.07799999999995]], "isOverall": false, "label": "Candidate Creation Thread Group", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.7683236E12, "title": "Active Threads Over Time"}},
        getOptions: function() {
            return {
                series: {
                    stack: true,
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 6,
                    show: true,
                    container: '#legendActiveThreadsOverTime'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                selection: {
                    mode: 'xy'
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : At %x there were %y active threads"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesActiveThreadsOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotActiveThreadsOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewActiveThreadsOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Active Threads Over Time
function refreshActiveThreadsOverTime(fixTimestamps) {
    var infos = activeThreadsOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotActiveThreadsOverTime"))) {
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesActiveThreadsOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotActiveThreadsOverTime", "#overviewActiveThreadsOverTime");
        $('#footerActiveThreadsOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var timeVsThreadsInfos = {
        data: {"result": {"minY": 819.0, "minX": 1.0, "maxY": 3243.4389140271483, "series": [{"data": [[2.0, 819.0], [3.0, 1628.0], [4.0, 835.0], [5.0, 1630.0], [6.0, 851.5], [7.0, 1676.0], [8.0, 1678.0], [9.0, 1678.0], [10.0, 1719.0], [11.0, 940.5], [12.0, 1718.0], [13.0, 1756.0], [14.0, 1751.0], [15.0, 1750.0], [16.0, 1754.0], [17.0, 1782.0], [18.0, 1780.0], [19.0, 1781.0], [20.0, 1779.0], [21.0, 1803.0], [22.0, 1800.0], [23.0, 1799.0], [24.0, 1798.0], [25.0, 1132.0], [26.0, 1851.0], [27.0, 1852.0], [28.0, 1889.0], [29.0, 1888.0], [30.0, 1888.0], [31.0, 1886.0], [33.0, 1935.0], [32.0, 1931.0], [35.0, 1970.0], [34.0, 1934.0], [37.0, 1971.0], [36.0, 1973.0], [39.0, 2004.0], [38.0, 1969.0], [41.0, 2004.0], [40.0, 2004.0], [43.0, 2035.0], [42.0, 2002.0], [45.0, 2038.0], [44.0, 2036.0], [47.0, 2071.0], [46.0, 2036.0], [49.0, 2072.0], [48.0, 2072.0], [50.0, 1502.0], [51.0, 2102.0], [53.0, 2104.0], [52.0, 2104.0], [55.0, 2130.0], [54.0, 2104.0], [57.0, 2148.0], [56.0, 2131.0], [59.0, 2182.0], [58.0, 2182.0], [61.0, 2186.0], [60.0, 2185.0], [63.0, 2219.0], [62.0, 2215.0], [67.0, 2259.0], [66.0, 2253.0], [65.0, 2219.0], [64.0, 2217.0], [71.0, 2297.0], [70.0, 2295.0], [69.0, 2257.0], [68.0, 2258.0], [75.0, 2339.0], [74.0, 2339.0], [73.0, 2338.0], [72.0, 2296.0], [79.0, 2376.0], [78.0, 2375.0], [77.0, 2372.0], [76.0, 2339.0], [83.0, 2411.0], [82.0, 2411.0], [81.0, 2409.0], [80.0, 2377.0], [87.0, 2441.0], [86.0, 2445.0], [85.0, 2442.0], [84.0, 2410.0], [91.0, 2477.0], [90.0, 2460.0], [89.0, 2461.0], [88.0, 2437.0], [95.0, 2580.2727272727275], [94.0, 2538.7999999999993], [93.0, 2507.0], [92.0, 2507.0], [99.0, 2807.158536585365], [98.0, 2689.25], [97.0, 2663.9473684210525], [96.0, 2624.3529411764703], [100.0, 3243.4389140271483], [1.0, 1599.0]], "isOverall": false, "label": "Create Candidate Request", "isController": false}, {"data": [[88.07799999999995, 2789.475999999999]], "isOverall": false, "label": "Create Candidate Request-Aggregated", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 100.0, "title": "Time VS Threads"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: { noColumns: 2,show: true, container: '#legendTimeVsThreads' },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s: At %x.2 active threads, Average response time was %y.2 ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesTimeVsThreads"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotTimesVsThreads"), dataset, options);
            // setup overview
            $.plot($("#overviewTimesVsThreads"), dataset, prepareOverviewOptions(options));
        }
};

// Time vs threads
function refreshTimeVsThreads(){
    var infos = timeVsThreadsInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTimeVsThreads");
        return;
    }
    if(isGraph($("#flotTimesVsThreads"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTimeVsThreads");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTimesVsThreads", "#overviewTimesVsThreads");
        $('#footerTimeVsThreads .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var bytesThroughputOverTimeInfos = {
        data : {"result": {"minY": 2787.1666666666665, "minX": 1.7683236E12, "maxY": 4112.166666666667, "series": [{"data": [[1.7683236E12, 2787.1666666666665]], "isOverall": false, "label": "Bytes received per second", "isController": false}, {"data": [[1.7683236E12, 4112.166666666667]], "isOverall": false, "label": "Bytes sent per second", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.7683236E12, "title": "Bytes Throughput Over Time"}},
        getOptions : function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity) ,
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Bytes / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendBytesThroughputOverTime'
                },
                selection: {
                    mode: "xy"
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y"
                }
            };
        },
        createGraph : function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesBytesThroughputOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotBytesThroughputOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewBytesThroughputOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Bytes throughput Over Time
function refreshBytesThroughputOverTime(fixTimestamps) {
    var infos = bytesThroughputOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotBytesThroughputOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesBytesThroughputOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotBytesThroughputOverTime", "#overviewBytesThroughputOverTime");
        $('#footerBytesThroughputOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimesOverTimeInfos = {
        data: {"result": {"minY": 2789.475999999999, "minX": 1.7683236E12, "maxY": 2789.475999999999, "series": [{"data": [[1.7683236E12, 2789.475999999999]], "isOverall": false, "label": "Create Candidate Request", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.7683236E12, "title": "Response Time Over Time"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average response time was %y ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Times Over Time
function refreshResponseTimeOverTime(fixTimestamps) {
    var infos = responseTimesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotResponseTimesOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesOverTime", "#overviewResponseTimesOverTime");
        $('#footerResponseTimesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var latenciesOverTimeInfos = {
        data: {"result": {"minY": 2788.695999999999, "minX": 1.7683236E12, "maxY": 2788.695999999999, "series": [{"data": [[1.7683236E12, 2788.695999999999]], "isOverall": false, "label": "Create Candidate Request", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.7683236E12, "title": "Latencies Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response latencies in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendLatenciesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average latency was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesLatenciesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotLatenciesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewLatenciesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Latencies Over Time
function refreshLatenciesOverTime(fixTimestamps) {
    var infos = latenciesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyLatenciesOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotLatenciesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesLatenciesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotLatenciesOverTime", "#overviewLatenciesOverTime");
        $('#footerLatenciesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var connectTimeOverTimeInfos = {
        data: {"result": {"minY": 0.19799999999999998, "minX": 1.7683236E12, "maxY": 0.19799999999999998, "series": [{"data": [[1.7683236E12, 0.19799999999999998]], "isOverall": false, "label": "Create Candidate Request", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.7683236E12, "title": "Connect Time Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getConnectTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average Connect Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendConnectTimeOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average connect time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesConnectTimeOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotConnectTimeOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewConnectTimeOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Connect Time Over Time
function refreshConnectTimeOverTime(fixTimestamps) {
    var infos = connectTimeOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyConnectTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotConnectTimeOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesConnectTimeOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotConnectTimeOverTime", "#overviewConnectTimeOverTime");
        $('#footerConnectTimeOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var responseTimePercentilesOverTimeInfos = {
        data: {"result": {"minY": 39.0, "minX": 1.7683236E12, "maxY": 3791.0, "series": [{"data": [[1.7683236E12, 3791.0]], "isOverall": false, "label": "Max", "isController": false}, {"data": [[1.7683236E12, 3698.8]], "isOverall": false, "label": "90th percentile", "isController": false}, {"data": [[1.7683236E12, 3776.98]], "isOverall": false, "label": "99th percentile", "isController": false}, {"data": [[1.7683236E12, 3748.95]], "isOverall": false, "label": "95th percentile", "isController": false}, {"data": [[1.7683236E12, 39.0]], "isOverall": false, "label": "Min", "isController": false}, {"data": [[1.7683236E12, 2709.5]], "isOverall": false, "label": "Median", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.7683236E12, "title": "Response Time Percentiles Over Time (successful requests only)"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Response Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentilesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Response time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentilesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimePercentilesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimePercentilesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Time Percentiles Over Time
function refreshResponseTimePercentilesOverTime(fixTimestamps) {
    var infos = responseTimePercentilesOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotResponseTimePercentilesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimePercentilesOverTime", "#overviewResponseTimePercentilesOverTime");
        $('#footerResponseTimePercentilesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var responseTimeVsRequestInfos = {
    data: {"result": {"minY": 40.0, "minX": 1.0, "maxY": 3664.0, "series": [{"data": [[2.0, 40.0], [4.0, 289.0], [1.0, 1848.0], [35.0, 3664.0], [36.0, 2805.0], [38.0, 2705.0], [20.0, 2610.5], [40.0, 2619.0], [48.0, 1826.5], [26.0, 3100.0], [13.0, 3104.0], [54.0, 2339.0]], "isOverall": false, "label": "Successes", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 54.0, "title": "Response Time Vs Request"}},
    getOptions: function() {
        return {
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Response Time in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: {
                noColumns: 2,
                show: true,
                container: '#legendResponseTimeVsRequest'
            },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median response time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesResponseTimeVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotResponseTimeVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewResponseTimeVsRequest"), dataset, prepareOverviewOptions(options));

    }
};

// Response Time vs Request
function refreshResponseTimeVsRequest() {
    var infos = responseTimeVsRequestInfos;
    prepareSeries(infos.data);
    if (isGraph($("#flotResponseTimeVsRequest"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeVsRequest");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimeVsRequest", "#overviewResponseTimeVsRequest");
        $('#footerResponseRimeVsRequest .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var latenciesVsRequestInfos = {
    data: {"result": {"minY": 39.5, "minX": 1.0, "maxY": 3664.0, "series": [{"data": [[2.0, 39.5], [4.0, 243.5], [1.0, 1847.0], [35.0, 3664.0], [36.0, 2805.0], [38.0, 2704.5], [20.0, 2610.0], [40.0, 2618.0], [48.0, 1826.0], [26.0, 3100.0], [13.0, 3104.0], [54.0, 2339.0]], "isOverall": false, "label": "Successes", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 54.0, "title": "Latencies Vs Request"}},
    getOptions: function() {
        return{
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Latency in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: { noColumns: 2,show: true, container: '#legendLatencyVsRequest' },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median Latency time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesLatencyVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotLatenciesVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewLatenciesVsRequest"), dataset, prepareOverviewOptions(options));
    }
};

// Latencies vs Request
function refreshLatenciesVsRequest() {
        var infos = latenciesVsRequestInfos;
        prepareSeries(infos.data);
        if(isGraph($("#flotLatenciesVsRequest"))){
            infos.createGraph();
        }else{
            var choiceContainer = $("#choicesLatencyVsRequest");
            createLegend(choiceContainer, infos);
            infos.createGraph();
            setGraphZoomable("#flotLatenciesVsRequest", "#overviewLatenciesVsRequest");
            $('#footerLatenciesVsRequest .legendColorBox > div').each(function(i){
                $(this).clone().prependTo(choiceContainer.find("li").eq(i));
            });
        }
};

var hitsPerSecondInfos = {
        data: {"result": {"minY": 8.333333333333334, "minX": 1.7683236E12, "maxY": 8.333333333333334, "series": [{"data": [[1.7683236E12, 8.333333333333334]], "isOverall": false, "label": "hitsPerSecond", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.7683236E12, "title": "Hits Per Second"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of hits / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendHitsPerSecond"
                },
                selection: {
                    mode : 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y.2 hits/sec"
                }
            };
        },
        createGraph: function createGraph() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesHitsPerSecond"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotHitsPerSecond"), dataset, options);
            // setup overview
            $.plot($("#overviewHitsPerSecond"), dataset, prepareOverviewOptions(options));
        }
};

// Hits per second
function refreshHitsPerSecond(fixTimestamps) {
    var infos = hitsPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if (isGraph($("#flotHitsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesHitsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotHitsPerSecond", "#overviewHitsPerSecond");
        $('#footerHitsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var codesPerSecondInfos = {
        data: {"result": {"minY": 8.333333333333334, "minX": 1.7683236E12, "maxY": 8.333333333333334, "series": [{"data": [[1.7683236E12, 8.333333333333334]], "isOverall": false, "label": "200", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.7683236E12, "title": "Codes Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendCodesPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "Number of Response Codes %s at %x was %y.2 responses / sec"
                }
            };
        },
    createGraph: function() {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesCodesPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotCodesPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewCodesPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Codes per second
function refreshCodesPerSecond(fixTimestamps) {
    var infos = codesPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotCodesPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesCodesPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotCodesPerSecond", "#overviewCodesPerSecond");
        $('#footerCodesPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var transactionsPerSecondInfos = {
        data: {"result": {"minY": 8.333333333333334, "minX": 1.7683236E12, "maxY": 8.333333333333334, "series": [{"data": [[1.7683236E12, 8.333333333333334]], "isOverall": false, "label": "Create Candidate Request-success", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.7683236E12, "title": "Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTransactionsPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                }
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTransactionsPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTransactionsPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewTransactionsPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Transactions per second
function refreshTransactionsPerSecond(fixTimestamps) {
    var infos = transactionsPerSecondInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTransactionsPerSecond");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotTransactionsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTransactionsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTransactionsPerSecond", "#overviewTransactionsPerSecond");
        $('#footerTransactionsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var totalTPSInfos = {
        data: {"result": {"minY": 8.333333333333334, "minX": 1.7683236E12, "maxY": 8.333333333333334, "series": [{"data": [[1.7683236E12, 8.333333333333334]], "isOverall": false, "label": "Transaction-success", "isController": false}, {"data": [], "isOverall": false, "label": "Transaction-failure", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.7683236E12, "title": "Total Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTotalTPS"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                },
                colors: ["#9ACD32", "#FF6347"]
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTotalTPS"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTotalTPS"), dataset, options);
        // setup overview
        $.plot($("#overviewTotalTPS"), dataset, prepareOverviewOptions(options));
    }
};

// Total Transactions per second
function refreshTotalTPS(fixTimestamps) {
    var infos = totalTPSInfos;
    // We want to ignore seriesFilter
    prepareSeries(infos.data, false, true);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotTotalTPS"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTotalTPS");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTotalTPS", "#overviewTotalTPS");
        $('#footerTotalTPS .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

// Collapse the graph matching the specified DOM element depending the collapsed
// status
function collapse(elem, collapsed){
    if(collapsed){
        $(elem).parent().find(".fa-chevron-up").removeClass("fa-chevron-up").addClass("fa-chevron-down");
    } else {
        $(elem).parent().find(".fa-chevron-down").removeClass("fa-chevron-down").addClass("fa-chevron-up");
        if (elem.id == "bodyBytesThroughputOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshBytesThroughputOverTime(true);
            }
            document.location.href="#bytesThroughputOverTime";
        } else if (elem.id == "bodyLatenciesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesOverTime(true);
            }
            document.location.href="#latenciesOverTime";
        } else if (elem.id == "bodyCustomGraph") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCustomGraph(true);
            }
            document.location.href="#responseCustomGraph";
        } else if (elem.id == "bodyConnectTimeOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshConnectTimeOverTime(true);
            }
            document.location.href="#connectTimeOverTime";
        } else if (elem.id == "bodyResponseTimePercentilesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimePercentilesOverTime(true);
            }
            document.location.href="#responseTimePercentilesOverTime";
        } else if (elem.id == "bodyResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeDistribution();
            }
            document.location.href="#responseTimeDistribution" ;
        } else if (elem.id == "bodySyntheticResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshSyntheticResponseTimeDistribution();
            }
            document.location.href="#syntheticResponseTimeDistribution" ;
        } else if (elem.id == "bodyActiveThreadsOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshActiveThreadsOverTime(true);
            }
            document.location.href="#activeThreadsOverTime";
        } else if (elem.id == "bodyTimeVsThreads") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTimeVsThreads();
            }
            document.location.href="#timeVsThreads" ;
        } else if (elem.id == "bodyCodesPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCodesPerSecond(true);
            }
            document.location.href="#codesPerSecond";
        } else if (elem.id == "bodyTransactionsPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTransactionsPerSecond(true);
            }
            document.location.href="#transactionsPerSecond";
        } else if (elem.id == "bodyTotalTPS") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTotalTPS(true);
            }
            document.location.href="#totalTPS";
        } else if (elem.id == "bodyResponseTimeVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeVsRequest();
            }
            document.location.href="#responseTimeVsRequest";
        } else if (elem.id == "bodyLatenciesVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesVsRequest();
            }
            document.location.href="#latencyVsRequest";
        }
    }
}

/*
 * Activates or deactivates all series of the specified graph (represented by id parameter)
 * depending on checked argument.
 */
function toggleAll(id, checked){
    var placeholder = document.getElementById(id);

    var cases = $(placeholder).find(':checkbox');
    cases.prop('checked', checked);
    $(cases).parent().children().children().toggleClass("legend-disabled", !checked);

    var choiceContainer;
    if ( id == "choicesBytesThroughputOverTime"){
        choiceContainer = $("#choicesBytesThroughputOverTime");
        refreshBytesThroughputOverTime(false);
    } else if(id == "choicesResponseTimesOverTime"){
        choiceContainer = $("#choicesResponseTimesOverTime");
        refreshResponseTimeOverTime(false);
    }else if(id == "choicesResponseCustomGraph"){
        choiceContainer = $("#choicesResponseCustomGraph");
        refreshCustomGraph(false);
    } else if ( id == "choicesLatenciesOverTime"){
        choiceContainer = $("#choicesLatenciesOverTime");
        refreshLatenciesOverTime(false);
    } else if ( id == "choicesConnectTimeOverTime"){
        choiceContainer = $("#choicesConnectTimeOverTime");
        refreshConnectTimeOverTime(false);
    } else if ( id == "choicesResponseTimePercentilesOverTime"){
        choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        refreshResponseTimePercentilesOverTime(false);
    } else if ( id == "choicesResponseTimePercentiles"){
        choiceContainer = $("#choicesResponseTimePercentiles");
        refreshResponseTimePercentiles();
    } else if(id == "choicesActiveThreadsOverTime"){
        choiceContainer = $("#choicesActiveThreadsOverTime");
        refreshActiveThreadsOverTime(false);
    } else if ( id == "choicesTimeVsThreads"){
        choiceContainer = $("#choicesTimeVsThreads");
        refreshTimeVsThreads();
    } else if ( id == "choicesSyntheticResponseTimeDistribution"){
        choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        refreshSyntheticResponseTimeDistribution();
    } else if ( id == "choicesResponseTimeDistribution"){
        choiceContainer = $("#choicesResponseTimeDistribution");
        refreshResponseTimeDistribution();
    } else if ( id == "choicesHitsPerSecond"){
        choiceContainer = $("#choicesHitsPerSecond");
        refreshHitsPerSecond(false);
    } else if(id == "choicesCodesPerSecond"){
        choiceContainer = $("#choicesCodesPerSecond");
        refreshCodesPerSecond(false);
    } else if ( id == "choicesTransactionsPerSecond"){
        choiceContainer = $("#choicesTransactionsPerSecond");
        refreshTransactionsPerSecond(false);
    } else if ( id == "choicesTotalTPS"){
        choiceContainer = $("#choicesTotalTPS");
        refreshTotalTPS(false);
    } else if ( id == "choicesResponseTimeVsRequest"){
        choiceContainer = $("#choicesResponseTimeVsRequest");
        refreshResponseTimeVsRequest();
    } else if ( id == "choicesLatencyVsRequest"){
        choiceContainer = $("#choicesLatencyVsRequest");
        refreshLatenciesVsRequest();
    }
    var color = checked ? "black" : "#818181";
    if(choiceContainer != null) {
        choiceContainer.find("label").each(function(){
            this.style.color = color;
        });
    }
}

