/**
 * Created by Jeff Reinhart on 2016-12-09.
 */
require(
    ["esri/map", "esri/layers/FeatureLayer", "esri/InfoTemplate",
     "esri/symbols/SimpleFillSymbol", "esri/symbols/SimpleLineSymbol",
     "esri/Color", "esri/renderers/UniqueValueRenderer",
     "dojo/domReady!"],
    function(Map, FeatureLayer, InfoTemplate,
             SimpleFillSymbol,SimpleLineSymbol,
             Color, UniqueValueRenderer){
        // initialize the map
        map = new Map("mapDiv", {
            center: [-93.6127, 46.5],
            zoom: 6,
            basemap: "gray"
        });
        map.on("load", addFeatureLayer);
        
        function addFeatureLayer() {
          // add counties
          var countiesLayer = new FeatureLayer("https://services.arcgis.com/P3ePLMYs2RVChkJx/ArcGIS/rest/services/USA_Counties_Generalized/FeatureServer/0",{
              // parameters here
              infoTemplate: new InfoTemplate(" ", "${NAME}")
          });
          
          // just MN
          countiesLayer.setDefinitionExpression("STATE_NAME = 'Minnesota'");
          
          // metro counties
          var metroCountiesArr = [
            "Anoka",
            "Carver",
            "Dakota",
            "Hennepin",
            "Ramsey",
            "Scott", 
            "Washington"
          ];
          
          // set default symbology
          var defaultSymbol = new SimpleFillSymbol().setStyle(SimpleFillSymbol.STYLE_NULL);
          defaultSymbol.outline.setStyle(SimpleLineSymbol.STYLE_NULL);
          
          // create renderer
          var renderer = new UniqueValueRenderer(defaultSymbol, "NAME");
          
          // function to get nth index of substring
          function getPosition(string, subString, index) {
             return string.split(subString, index).join(subString).length;
          }

          // update symbology based on python script content
          $.get("../parcels_main.py", function(data){
            var startIndex;
            var nextBraceIndex;
            var scriptText;
            var nextString;
            var countyName;
            var runBool;
            var runCount = 87;
            
            // prep first string
            startIndex = data.indexOf("countyRunList = [")+28;
            scriptText = data.slice(startIndex);
            
            while(runCount > 0){
              // get county name and whether mapping is completed (as string)
              nextBraceIndex = scriptText.indexOf("]");
              nextString = scriptText.slice(0,nextBraceIndex);
              countyName = nextString.slice(getPosition(nextString, " ", 4)).slice(2,-1)
              runBool = nextString.slice(0,4);
              // update renderer
              if (runBool == "True") {
                // has fields mapped and processing completed
                renderer.addValue(countyName, new SimpleFillSymbol().setColor(new Color([0, 0, 255, 1.0])));
              } else if ($.inArray(countyName, metroCountiesArr) > -1) {
                // is a metro county
                renderer.addValue(countyName, new SimpleFillSymbol().setColor(new Color([0, 0, 255, 1.0])));
              } else {
                // not completed
                renderer.addValue(countyName, new SimpleFillSymbol().setColor(new Color([255, 102, 0, 1.0])));
              }
              // pop county from string for next and drop count
              nextIndex = scriptText.indexOf("[",1);
              scriptText = scriptText.slice(nextIndex+1); 
              runCount -= 1;
            };
          }); // end $.get
          
          // set renderer and add layer
          countiesLayer.setRenderer(renderer);
          map.addLayer(countiesLayer);
          
        } // end function addFeatureLayer
    }); // end require