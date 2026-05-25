
#target photoshop

function calculateArea(points) {
    var area = 0;
    var n = points.length;
    for (var i = 0; i < n; i++) {
        var j = (i + 1) % n;
        area += points[i].anchor[0] * points[j].anchor[1];
        area -= points[j].anchor[0] * points[i].anchor[1];
    }
    area = Math.abs(area) / 2.0;
    return area;
}

function main() {
    if (!app.documents.length) {
        alert("No document open.");
        return;
    }

    var doc = app.activeDocument;
    var paths = doc.pathItems;
    if (paths.length === 0) {
        alert("No paths found in the Paths panel.");
        return;
    }

    var resolution = doc.resolution; // pixels per inch
    var results = "Path Areas (in pixels):\\n";

    for (var i = 0; i < paths.length; i++) {
        var path = paths[i];
        var subPathItems = path.subPathItems;
        var totalArea = 0;

        for (var j = 0; j < subPathItems.length; j++) {
            var subPath = subPathItems[j];
            if (!subPath.closed) continue; // Only calculate area for closed paths
            var points = subPath.pathPoints;
            totalArea += calculateArea(points);
        }

        results += path.name + ": " + totalArea.toFixed(2) + " px²\\n";
    }

    // Save results to a text file on desktop
    var desktop = Folder.desktop;
    var file = new File(desktop + "/path_areas.txt");
    file.open("w");
    file.write(results);
    file.close();

    alert("Area calculation complete. Results saved to path_areas.txt on your desktop.");
}

main();
