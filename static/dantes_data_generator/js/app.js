// Grab/create any variables needed
var canvas = document.getElementById('graph-canvas');
var ctx = canvas.getContext('2d');
var width = canvas.width;
var height = canvas.height;
var addPointsSetting = document.getElementById('points-action-add');
var interpLinearSetting = document.getElementById('interp-linear');
var outputStyleCSV = document.getElementById('output-style-csv');
var formElement = document.getElementById('calculation-form');
var pointValueElement = document.getElementById('point-value-container');
var curveValues = [];
var pointsChanged = true;
// Values for later use
var POINT_COLOR = 'rgba(0, 0, 150, 1)';
var POINT_BORDER_COLOR = 'rgba(0, 0, 0, 1)';
var POINT_RADIUS = 5;
var AXES_DISTANCE = 50;
var DRAW_WIDTH = width - AXES_DISTANCE;
var DRAW_HEIGHT = height - AXES_DISTANCE;
var AXES_COLOR = 'rgba(255, 0, 0, 1)';
var TEXT_COLOR = 'rgba(0, 0, 0, 1)';
var TEXT_HEIGHT = 15;
var AXES_CORNER = [AXES_DISTANCE, height - AXES_DISTANCE];
var LINE_SEGMENT_COLOR = 'rgba(0, 200, 0, 1)';
var LINE_SEGMENT_WIDTH = 2;
var BORDER_COLOR = 'rgba(150, 150, 150, 1)';
// [x-start-x, x-start-y, x-end-x, x-end-y, y-start-x, y-start-y, y-end-x, y-end-y]
var axesLabelLocations = [
    AXES_DISTANCE,
    height - AXES_DISTANCE + TEXT_HEIGHT + 5,
    width - AXES_DISTANCE,
    height - AXES_DISTANCE + TEXT_HEIGHT + 5,
    AXES_DISTANCE - 5,
    height - AXES_DISTANCE,
    AXES_DISTANCE - 5,
    AXES_DISTANCE
];
var xMin = document.getElementById('x-min-field');
var xMax = document.getElementById('x-max-field');
var yMin = document.getElementById('y-min-field');
var yMax = document.getElementById('y-max-field');
var pointList = [];  // List of points in form [[x0, y0], [x1, y1], ...]


// Functions

// Drawing-related functions
// Draws an empty canvas
function clearCanvas() {
    ctx.clearRect(0, 0, width, height);
}
// Draws the axes
function drawAxes() {
    // Setup style options
    ctx.strokeStyle = AXES_COLOR;
    ctx.fillStyle = AXES_COLOR;
    ctx.lineWidth = 2;
    // Draw x-axis
    ctx.beginPath();
    ctx.moveTo(AXES_DISTANCE, height - AXES_DISTANCE);
    ctx.lineTo(width, height - AXES_DISTANCE);
    ctx.stroke();
    // Draw y-axis
    ctx.beginPath();
    ctx.moveTo(AXES_DISTANCE, height - AXES_DISTANCE);
    ctx.lineTo(AXES_DISTANCE, 0);
    ctx.stroke();
    // Draw small circle at the intersection
    ctx.beginPath();
    ctx.arc(AXES_CORNER[0], AXES_CORNER[1], 2, 0, 2 * Math.PI);
    ctx.fill();
}
// Draws the Axes labels
function drawAxesLabels() {
    // Setup style options
    ctx.fillStyle = TEXT_COLOR;
    ctx.font = '' + TEXT_HEIGHT + 'px sans-serif';
    // X-Axis labels
    ctx.textAlign = 'left';
    ctx.fillText(xMin.value, axesLabelLocations[0], axesLabelLocations[1]);
    ctx.fillText(xMax.value, axesLabelLocations[2], axesLabelLocations[3]);
    // Y-Axis labels
    ctx.textAlign = 'right';
    ctx.fillText(yMin.value, axesLabelLocations[4], axesLabelLocations[5]);
    ctx.fillText(yMax.value, axesLabelLocations[6], axesLabelLocations[7]);
}
// Draw a point
function drawPoint(x, y) {
    ctx.fillStyle = POINT_COLOR;
    ctx.strokeStyle = POINT_BORDER_COLOR;
    ctx.beginPath();
    ctx.arc(x, y, POINT_RADIUS, 0, 2 * Math.PI)
    ctx.fill();
    ctx.stroke();
}
// Draw all points
function drawAllPoints() {
    for (var pnt of pointList) {
        drawPoint(pnt[0], pnt[1]);
    }
}
// Draw a single line segment
function drawSegment(x1, y1, x2, y2) {
    ctx.strokeStyle = LINE_SEGMENT_COLOR;
    ctx.lineWidth = LINE_SEGMENT_WIDTH;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
}
// Draw lines between the points
function drawLines() {
    plLength = pointList.length;
    if (plLength > 0) {
        drawSegment(AXES_DISTANCE, pointList[0][1], pointList[0][0], pointList[0][1]);
        for (var i = 0; i < plLength - 1; i++) {
            drawSegment(pointList[i][0], pointList[i][1], pointList[i + 1][0], pointList[i + 1][1]);
        }
        drawSegment(pointList[plLength - 1][0], pointList[plLength - 1][1], width, pointList[plLength - 1][1]);
    }
}
// Draw curves between points
function drawCurves() {
    function performDraw() {
        // Preliminary
        ctx.strokeStyle = LINE_SEGMENT_COLOR;
        ctx.lineWidth = LINE_SEGMENT_WIDTH;
        ctx.beginPath();

        // Draw the tiny segments
        ctx.moveTo(curveValues[0][0], curveValues[0][1]);
        var i;
        for(i = 0; i < curveValues.length; i++) {
            ctx.lineTo(curveValues[i][0], curveValues[i][1]);
        }
        ctx.stroke();
        drawAllPoints();
    }
    // Calculate points to make tiny segments from
    if (pointsChanged && pointList.length > 1) {
        submitCalculationAjax(false, performDraw);
        pointsChanged = false;
    } else {
        performDraw();
    }
}
// Fill border area
function fillBorder() {
    ctx.fillStyle = BORDER_COLOR;
    ctx.fillRect(0, 0, AXES_DISTANCE, height);
    ctx.fillRect(0, DRAW_HEIGHT, width, AXES_DISTANCE);
}
// Redraw everything
function updateCanvas() {
    updatePointValues();
    clearCanvas();
    fillBorder();
    drawAxes();
    drawAxesLabels();
    drawAllPoints();
    if (interpLinearSetting.checked) {
        drawLines();
        drawAllPoints();
    } else {
        drawCurves();
    }
}

// Non-Drawing functions
// Handles the AJAX call that performs the calculation server-side.
function submitCalculationAjax(writeResults, callback) {
    if (typeof writeResults == 'undefined') writeResults = true;
    // Preliminary steps
    var xhr = new XMLHttpRequest();
    var form_values = new FormData(formElement);
    var result_element = document.getElementById('data-generator-results');
    // Get the values out of the form and gather any other information needed
    result_json = {}
    for (var pair of form_values.entries()) {
        result_json[pair[0]] = pair[1];
    }
    result_json['pointValues'] = getPointCoordinates();

    // Necessary XMLHttpRequest steps
    xhr.open('POST', '', true);
    xhr.setRequestHeader('content-type', 'application/json');
    //xhr.setRequestHeader("X-CSRFToken", document.getElementsByName('csrfmiddlewaretoken')[0].value);

    // What to do when actually calling the POST
    xhr.onload = function () {
        if(this.status==200) {
            var result = JSON.parse(this.responseText)
            if (writeResults) {
                if (outputStyleCSV.checked) {
                    result_element.innerHTML = result['data']
                } else {
                    result_element.innerHTML = JSON.stringify(result['data'])
                }
            }
            curveValues = reversePointCoordinates(result['curveValues'])
            if (typeof callback == 'function') callback();
        }
    };
    // Error handling
    xhr.onerror = function () {
        console.log('Error with function.')
    }
    // Sending all of the data
    var json_str = JSON.stringify(result_json)
    console.log(json_str)
    xhr.send(json_str);
}

// Copies data to the clipboard when the button to do that is pressed
function copyDataToClipboard() {
    var data = document.getElementById('data-generator-results');
    data.select();
    document.execCommand('copy');
}
// Adds a point to the point list.
function addPoint(x, y) {
    pointList.push([x, y])
    pointList.sort(function(a, b){return a[0] - b[0]})
    pointsChanged = true;
}
// Removes a point close to a particular location
function removePoint(x, y) {
    var i;
    for (i in pointList) {
        if (Math.hypot(x - pointList[i][0], y - pointList[i][1]) <= POINT_RADIUS) {
            pointList.splice(i, 1);
            break;
        }
    }
    pointList.sort(function(a, b){return a[0] - b[0]})
    pointsChanged = true;
}
// Handles canvas clicks
function onCanvasClick(e) {
    // Whether to add or remove points
    var pointsSettingValue = addPointsSetting.checked ? 'add' : 'remove';
    // Get the click coordinates relative to the canvas
    var rect = canvas.getBoundingClientRect();
    var xVal = e.clientX - rect.left;
    var yVal = e.clientY - rect.top;
    // Perform the action needed
    if (xVal >= AXES_CORNER[0] && yVal <= AXES_CORNER[1]) {
        if (pointsSettingValue == 'add') {
            addPoint(xVal, yVal);
        } else if (pointsSettingValue == 'remove') {
            removePoint(xVal, yVal);
        }
        updateCanvas();
    }
}
// Translates on-canvas point coordinates to mathematical coordinates for the given axis values
function getPointCoordinates() {
    var resultList = [];
    var xMinVal = parseFloat(xMin.value);
    var xMaxVal = parseFloat(xMax.value);
    var yMinVal = parseFloat(yMin.value);
    var yMaxVal = parseFloat(yMax.value);
    var mathWidth = xMaxVal - xMinVal;
    var mathHeight = yMaxVal - yMinVal;
    for (var pnt of pointList) {
        resultList.push([
            (pnt[0] - AXES_DISTANCE) / DRAW_WIDTH * mathWidth + xMinVal,
            (DRAW_HEIGHT - pnt[1]) / DRAW_HEIGHT * mathHeight + yMinVal
        ]);
    }
    return resultList
}
// Reverses the functionality of getPointCoordinates()
function reversePointCoordinates(pointInput) {
    var resultList = [];
    var xMinVal = parseFloat(xMin.value);
    var xMaxVal = parseFloat(xMax.value);
    var yMinVal = parseFloat(yMin.value);
    var yMaxVal = parseFloat(yMax.value);
    var mathWidth = xMaxVal - xMinVal;
    var mathHeight = yMaxVal - yMinVal;
    for (var pnt of pointInput) {
        resultList.push([
            (pnt[0] - xMinVal) / mathWidth * DRAW_WIDTH + AXES_DISTANCE,
            (yMinVal - pnt[1]) / mathWidth * DRAW_HEIGHT + DRAW_HEIGHT
        ]);
    }
    return resultList
}
// Updates visuals for the current point values
function updatePointValues() {
    console.log(pointList)
    pointValueElement.innerHTML = JSON.stringify(getPointCoordinates(pointList));
}

// Add event listeners and perform any initial setup tasks
document.getElementById('calculation-form').addEventListener('submit', function (e) {
    e.preventDefault();
    submitCalculationAjax();
    document.getElementById('copy-clipboard').disabled = false;
});
document.getElementById('copy-clipboard').addEventListener('click', copyDataToClipboard);
canvas.addEventListener('click', onCanvasClick);
for (inputElement of formElement.getElementsByTagName('input')) {
    inputElement.addEventListener('change', updateCanvas);
}
updateCanvas();