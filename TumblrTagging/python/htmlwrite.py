''' Authors: Brooke Boatman and Rebecca Gold
    Date: December 2015
    Methods to produce the wrapping html for voronoi tesselations
    Pulled out of code for readability - I realise there are so many
    better ways to do this, but for time's sake this was the most doable
'''

def getTop():
    return """
    <!DOCTYPE HTML>

    <html>
        <head>
            <title>WikiBrainMap</title>
            <script type="text/javascript" src="../d3/d3.v3.min.js"></script>
        </head>

        <body>
        <script type="text/javascript">
            var w = 3000;
            var h = 3000;

            var dataset = [
    """
def getBottom():
    return """
     ];
                  function pastelColors(hue, lit){
            var pastel = 'hsl(' + hue + ', 100%, '+ lit +'%)';
            return pastel
        }
            //Create SVG element
            var svg = d3.select("body")
                    .append("svg")
                    .attr("width", w)
                    .attr("height", h);

            svg.selectAll("path")
                .data(d3.geom.voronoi(dataset))
                .enter().append("svg:path")
                .attr("d", function(d) {if(d && d.join) { return "M" + d.join("L") + "Z"; }})
                .attr("stroke", "gray")
                .attr("stroke-width", .5)
                .attr("fill", function(d) { 
                    console.log(d);
                    if (d == undefined){
                        return 360;
                    }
                    return pastelColors(d.point[3], d.point[4])});

            svg.selectAll("circle")
                    .data(dataset)
                    .enter()
                    .append("circle")
                    .attr("cx", function(d) {
                        return d[0];
                    })
                    .attr("cy", function(d) {
                        return d[1];
                    })
                    .attr("r", function(d) {
                        return 1;
                    })
                    .attr("fill", "gray");

            svg.selectAll("text")
                .data(dataset)
                .enter()
                .append("text")
                .text(function(d) {
                    return d[2];
                })
                .attr("x", function(d) {
                    return d[0] + 2;
                })
                .attr("y", function(d) {
                    return d[1] + 2;
                })
                .attr("font-size", "5px")
                .attr("fill", "black")
                .attr("font-family", "sans-serif");   
        </script>
        </body>
    </html>
    """