//LANGUAGE DEPENDENT
var attemps = 0;
function showAlertDialog(correct, qId){
	var text = correct ? "Bravo, la réponse est correcte." : "Cette réponse n'est pas correcte.";
	//close existing dialogs
	if (alertDialog != null){
		closeAlertDialog(qId);
	}
	//dialog
	alertDialog = document.createElement('div');
	alertDialog.id = 'alertDialog' + qId;
	alertDialog.style.cssText = "position:fixed;width:400px;top: 50%;left: 50%;margin-left: -200px; margin-top: -40px; background: #6b6a63; padding: 3px;";
	//content
	contentDiv = document.createElement('div');
	contentDiv.style.cssText = "background:#fff;padding:20px;text-align:center;";
	contentDiv.appendChild(document.createTextNode(text));
	//buttons
	var buttons = document.createElement("div");
	buttons.style.textAlign = "center";
	buttons.style.marginTop = "20px";
	buttons.style.width = "100%";
	contentDiv.appendChild(buttons);
	buttons.appendChild(createButton("Réinitialiser", "resetExercise", qId, true));
	if (attemps > 0 && attemps < 2 || correct){
		var hint = document.getElementById('explanation' + qId).cloneNode(true);
		hint.id = "dialog_hint" + qId;
		hint.style.display = "none";
		if (hint.innerHTML.trim().length > 0){
			contentDiv.appendChild(hint);
			buttons.appendChild(createButton("Explication", "toggleHelp", qId, false));
		}
	}
	if (correct){
		buttons.appendChild(createButton("Fermer", "", qId, true));
		attemps = 0;
	}else{
		if (attemps < 2){
			buttons.appendChild(createButton("Continuer", "", qId, true));
		}
		attemps++;
	}
	alertDialog.appendChild(contentDiv);
	document.getElementsByTagName('body')[0].appendChild(alertDialog);
	el = document.getElementById('submitButton' + qId);
	if (el)
		el.disabled = true;
}

//OTHER FUNCTIONS
function showHint(qId){
	if (alertDialog != null){
		closeAlertDialog(qId);
	}
	//dialog
	alertDialog = document.createElement('div');
	alertDialog.id = 'alertDialog' + qId;
	alertDialog.style.cssText = "position:fixed;width:400px;top: 50%;left: 50%;margin-left: -200px; margin-top: -40px; background: #6b6a63; padding: 3px;";
	//content
	contentDiv = document.createElement('div');
	contentDiv.style.cssText = "background:#fff;padding:20px 20px 0px 20px;text-align:center;";
	alertDialog.appendChild(contentDiv);
	//message
	el = document.getElementById('hint' + qId).cloneNode(true);
	el.className = "";
	el.style.display = "block";
	contentDiv.appendChild(el);
	//buttons
	var buttons = document.createElement("div");
	buttons.style.textAlign = "center";
	buttons.style.marginTop = "20px";
	buttons.style.width = "100%";
	contentDiv.appendChild(buttons);
	buttons.appendChild(createButton("OK", "hideHint", qId, true));
	//finalize
	document.getElementsByTagName('body')[0].appendChild(alertDialog);
	el = document.getElementById('hintButton' + qId);
	el.disabled = true;
}

function hideHint(qId){
	el = document.getElementById('hintButton' + qId);
	el.disabled = null;
}

function validateCheckBox(names, values, qId) {
	correct = true;
	for (var i = 0; i < names.length; i++) {
		checkbox = document.getElementById(names[i]);
		if(checkbox != null){
			if((values[i] === "true") != checkbox.checked)
				correct = false;
		}else{
			//alert("Error");
			//return;
		}
	}
	showAlertDialog(correct, qId);
}

function validateRadioButton(names, values, qId) {
	correct = true;
	for (var i = 0; i < names.length; i++) {
		checkbox = document.getElementById(names[i]);
		if(checkbox != null){
			if((values[i] === "true") != checkbox.checked)
				correct = false;
		}else{
			//alert("Error");
			//return;
		}
	}
	showAlertDialog(correct, qId);
}

function checkValueInRange(lowerLimit, upperLimit, elementId, qId){
	element = document.getElementById(elementId);
	var correct = element.value >= lowerLimit && element.value <= upperLimit;
	showAlertDialog(correct, qId);
}

function checkBoolean(val, qId){
	showAlertDialog(val, qId);
}

var alertDialog = null;

function closeAlertDialog(qId){
	if(alertDialog = null)
		return;
	el = document.getElementById('alertDialog' + qId);
	el.parentNode.removeChild(el);
	delete alertDialog;
    alertDialog = null;
	el = document.getElementById('submitButton' + qId);
	if (el)
		el.disabled = null;
	el = document.getElementById('hintButton' + qId);
	if (el)
		el.disabled = null;
}

function toggleHelp(qId){
	var hint = document.getElementById("dialog_hint" + qId);
	if (hint.style.display.indexOf("none") == 0)
		hint.style.display = "block";
	else
		hint.style.display = "none";
}

function createButton(label, functionName, qId, closeOnclick){
	var button = document.createElement("button");
	if (functionName && functionName.trim().length > 0)
		functionName += "('" + qId + "');";
	if (closeOnclick)
		functionName += "closeAlertDialog('" + qId + "');";
	button.setAttribute("onclick", functionName);
	button.innerHTML = label;
	button.style.margin = "10px";
	return button;
}

function checkPickSpot(spots, values, qId){
	correct = true;
	var spot;
	for (var i = 0; i < spots.length; i++) {
		spot = document.getElementById(spots[i]);
		if(spot != null){
			if((values[i] === "true") && ((spot.className + "").indexOf("exercise_interactive_area_selected") < 0) ||
					(values[i] === "false") && ((spot.className + "").indexOf("exercise_interactive_area_selected") >= 0))
				correct = false;
		}else{
			//alert("Error");
			//return;
		}
	}
	showAlertDialog(correct, qId);
}

function toggleInteractiveArea(area){
	if ((area.className + "").indexOf("exercise_interactive_area_selected") >= 0)
		area.className = "exercise_interactive_area";
	else
		area.className = "exercise_interactive_area_selected";
}

//drag and drop
var draggableElement = null;
var sourceElement = null;
var sourceParent = null;
var targetArea = null;

var sourceElementCN = "";
var sourceAreaCN = "";
var targetAreaCN = "";

function initDraggable(idDraggable, sourceElementClassName, sourceAreaClassName, targetAreaClassName) {
  draggableElement = document.getElementById(idDraggable);
  draggableElement.setAttribute('touch-action', 'none');
  sourceElementCN = sourceElementClassName;
  sourceAreaCN = sourceAreaClassName;
  targetAreaCN = targetAreaClassName;

  var divs = document.getElementsByTagName("div");
  for (var d = 0; d < divs.length; d++) {
      var div = divs[d];
      if(div.className && div.className.indexOf(sourceElementCN) >= 0){
          div.setAttribute('touch-action', 'none');
          div.addEventListener('pointerdown', function (e) {
              selectDraggable(this);
          });
      }
  }

  var body = document.body;
  body.setAttribute('touch-action', 'none');
  body.addEventListener('pointermove', function (e) {
      moveDraggable(e);
  });
  body.addEventListener('pointerup', function (e) {
      dropElement();
  });
}

function selectDraggable(element) {
  cleanParentFromSource(draggableElement);
  sourceElement = element;
  sourceParent = element.parentNode;
  draggableElement.appendChild(element);
  draggableElement.style.width = 100 + 'px';
  draggableElement.style.height = 100 + 'px';
}


function moveDraggable(e) {
  var mouse = getCoordinates(e);
  var width = draggableElement.offsetWidth;
  var height = draggableElement.offsetHeight;

  draggableElement.style.left = (mouse.dx - width/2) + "px";
  draggableElement.style.top = (mouse.dy- height/2) + "px";


  var mouseOverElement = document.elementFromPoint(mouse.dx, mouse.dy);
  while (!mouseOverElement.className || (mouseOverElement.className.indexOf(targetAreaCN) < 0 && mouseOverElement.className.indexOf(sourceAreaCN) < 0)) {
      mouseOverElement = mouseOverElement.parentNode;
      if (mouseOverElement == null) {
          targetArea = null;
          return;
      }
  }
  //console.log(mouseOverElement + " " + targetArea);
  targetArea = mouseOverElement;
}

function dropElement() {
  if (targetArea) {
      if (sourceElement) {
          if (targetArea.className && targetArea.className.indexOf(targetAreaCN) >= 0) {
              cleanParentFromSource(targetArea);
              targetArea.appendChild(sourceElement);
          } else if (targetArea.className && targetArea.className.indexOf(sourceAreaCN) >= 0) {
              if (containElementWithClassName(targetArea, sourceElementCN)) {
                  goInPool(sourceElement);
              } else {
                  targetArea.appendChild(sourceElement);
              }
          }
      }
  } else {
      if (sourceElement) {
          goInPool(sourceElement);
      }
  }
  sourceParent = null;
  sourceElement = null;
  draggableElement.style.width = 0 + 'px';
  draggableElement.style.height = 0 + 'px';
}

function goInPool(element) {
  var sourceAreaDivs = document.getElementsByClassName(sourceAreaCN);
  for (var d = 0; d < sourceAreaDivs.length; d++) {
      var sourceAreaDiv = sourceAreaDivs[d];
      if (!containElementWithClassName(sourceAreaDiv, sourceElementCN)) {
          sourceAreaDiv.appendChild(element);
      }
  }
}

function cleanParentFromSource(parentElement) {
  var sourceElements = parentElement.getElementsByClassName(sourceElementCN);
  for (var d = 0; d < sourceElements.length; d++) {
      var sourceElement = sourceElements[d];
      goInPool(sourceElement);
  }
}

function containElementWithClassName(element, className) {
  var elementList = element.getElementsByClassName(className);
  if (elementList.length > 0) {
      return true;
  }
  return false;
}

function moveObject(sources, targets, qId){
	correct = true;
	var target;
	for (var i = 0; i < targets.length; i++) {
		target = document.getElementById(targets[i]);
		if (target != null){
			if (!target.className){
				target.className = "";
			}else{
				target.className = target.className.replace(" exercise_area_wrong", "");
				target.className = target.className.replace(" exercise_area_good", "");
			}
			if (target.childNodes.length == 0){
				correct = false;
				target.className += " exercise_area_wrong";
				continue;
			}
			for (var c = 0; c < target.childNodes.length; c++){
				var targetId = "prim_" + target.id;
				var primitiveId = ("" + target.childNodes[c].id).replace("source", "target");
				if (targetId.length != primitiveId.length || primitiveId.indexOf(targetId) != 0){
					target.className += " exercise_area_wrong";
					correct = false;
				}else{
					target.className += " exercise_area_good";
				}
			}
		}else{
			//alert("Error");
			//return;
		}
	}
	showAlertDialog(correct, qId);
}


//create arrows
var arrowX;
var arrowY;
var sourcePrimitive = null;
var sourceArea = null;
var targetArea = null;
var result = [];

function checkArrows(sources, targets, qId){
	correct = true;
	if (result.length != sources.length){
		correct = false;
	}
	for (var r = 0; r < sources.length; r++) {
		if (!result[r]){
			continue;
		}
		var target = document.getElementById(result[r].target);
		if (target){
			if (!target.className){
				target.className = "";
			}else{
				target.className = target.className.replace(" exercise_area_wrong", "");
				target.className = target.className.replace(" exercise_area_good", "");
			}
		}
		if (!result[r].target || !result[r].source){
			correct = false;
			if (target) //really necessary?
				target.className += " exercise_area_wrong";
			continue;
		}
		var index1 = result[r].source.substring("area_".length);
		index1 = index1.substring(0, index1.indexOf("_"));
		var index2 = result[r].target.substring("area_".length);
		index2 = index2.substring(0, index2.indexOf("_"));
		if (target){
			if (index1 != index2){
				correct = false;
				target.className += " exercise_area_wrong";
			}else{
				target.className += " exercise_area_good";
			}
		}
	}
	//fix wrong source
	for (var s = 0; s < sources.length; s++) {
		var id = sources[s].replace("source", "target");
		var target = document.getElementById(id);
		if (!target)
			continue;
		if (!target.className || target.className.indexOf("exercise_area_wrong") < 0 && target.className.indexOf("exercise_area_good") < 0){
			target.className += " exercise_area_wrong";
		}
	}
	showAlertDialog(correct, qId);
}

var isChrome = navigator.userAgent.toLowerCase().indexOf("chrome") > 0;
function getCoordinates(e){
    e = e || window.event;
    var x;
	var y;
	if (isChrome){
		x = e.x;
		y = e.y;
	}else{
		x = e.pageX + document.body.scrollLeft;
		y = e.pageY + document.body.scrollTop;
	}
	return {dx: x, dy: y};
}

function createArrow(e, canvasId, primitive) {	
	 var canvas = document.getElementById(canvasId);
	 var coords = getElementOffset(canvas);
	 var mouse = getCoordinates(e);
	 sourceArea = primitive;
	    arrowX = mouse.dx - coords.dx;
	    arrowY = mouse.dy - coords.dy;
	 if (!sourcePrimitive)
	  sourcePrimitive = primitive;
	 drawArrows(canvasId);
	 e.preventDefault();
}

function moveArrow(e, canvasId, source){
	if (!sourcePrimitive)
		return;
	var canvas = document.getElementById(canvasId);
	var coords = getElementOffset(canvas);
	var mouse = getCoordinates(e);
    arrowX = mouse.dx - coords.dx;
    arrowY = mouse.dy - coords.dy;
	drawArrows(canvasId);
	if (source != sourceArea)
		drawInteractor(canvasId);
}

function destroyArrow(canvasId){
	if (!sourceArea)
		return;
	if (sourceArea.className && sourceArea.className.indexOf('exercise_source_area_selected') >= 0)
		sourceArea.className = sourceArea.className.replace("exercise_source_area_selected", "");
	sourceArea = null;
	sourcePrimitive = null;
	drawArrows(canvasId);
}

function joinArrow(canvasId, target){
	var record;
	if (sourceArea == null || targetArea == null)
		return;
	for (var r = 0; r < result.length; r++){
		if (result[r].source.indexOf(sourceArea.id) == 0){
			record = result[r];
			break;
		}
	}
	for (var r = 0; r < result.length; r++){
		if (result[r].target && result[r].target.indexOf(targetArea.id) == 0){
			result[r].target = null;
			break;
		}
	}
	if (!record){
		record = new Object();
		result[result.length] = record;
	}
	record.source = sourceArea.id;
	record.target = targetArea.id;	
	if (sourceArea.className && sourceArea.className.indexOf('exercise_source_area_selected') >= 0)
		sourceArea.className = sourceArea.className.replace("exercise_source_area_selected", "");
	if (targetArea.className && targetArea.className.indexOf('exercise_target_area_selected') >= 0)
		targetArea.className = targetArea.className.replace("exercise_target_area_selected", "");
	sourcePrimitive = null;
	targetPrimitive = null;
	drawArrows(canvasId);
}

function enterSourceArea(event, area){
	if (sourceArea && sourceArea == area || sourcePrimitive){
		return;
	}
    event = event || window.event;
	if (!sourcePrimitive && area.className.indexOf('exercise_source_area_selected') < 0)
		area.className += " exercise_source_area_selected";
	if (sourceArea){
		sourceArea.className = sourceArea.className.replace(" exercise_source_area_selected", "");
	}
	sourceArea = area;
	event.preventDefault();
}

function exitSourceArea(event){
    if (sourcePrimitive){
    	event.preventDefault();
    	return;
    }
	if (sourceArea && sourceArea.className && sourceArea.className.indexOf('exercise_source_area_selected') >= 0)
		sourceArea.className = sourceArea.className.replace("exercise_source_area_selected", "");
	sourceArea = null;
}

function onSourceArea(e, canvasId){
	if (!sourcePrimitive)
		return;
	var mouse = getCoordinates(e);
    arrowX = mouse.dx;
    arrowY = mouse.dy;
	e.preventDefault();
}

function enterTargetArea(event, area){
    event = event || window.event;
	if (sourcePrimitive && area.className.indexOf('exercise_target_area_selected') < 0)
		area.className += " exercise_target_area_selected";
	if (targetArea && targetArea != area){
		targetArea.className = targetArea.className.replace(" exercise_target_area_selected", "");
	}
	targetArea = area;
	event.preventDefault();
}

function exitTargetArea(event){
	if (targetArea && targetArea.className && targetArea.className.indexOf('exercise_target_area_selected') >= 0)
		targetArea.className = targetArea.className.replace("exercise_target_area_selected", "");
	targetArea = null;
}

function onTargetArea(e, canvasId){
	if (!sourcePrimitive)
		return;
	var mouse = getCoordinates(e);
    arrowX = mouse.dx;
    arrowY = mouse.dy;
	e.preventDefault();
}

function drawInteractor(canvasId){
	var canvas = document.getElementById(canvasId);
	var context = canvas.getContext("2d");
	context.lineWidth = 5;
	context.strokeStyle = "rgba(243, 111, 33, 1)";
	context.setLineDash([]);
	var sourceArea = sourcePrimitive;
	var x1 = cropPercent(sourceArea.style.left, canvas.width);
	var y1 = cropPercent(sourceArea.style.top, canvas.height);
	var w = cropPercent(sourceArea.style.width, canvas.width);
	var h = cropPercent(sourceArea.style.height, canvas.height);
	var x2 = x1 + w;
	var y2 = y1 + h;
	var cx = x1 + w / 2;
	var cy = y1 + h / 2;
	var angle = Math.atan2(arrowY - cy, arrowX - cx);
	var PI_2 = Math.PI * 1 / 2;
	var p1;
	//calculate source intersection
	var sourceAngle = Math.atan2(y2 - y1, x2 - x1);
	if (sourceAngle >= angle && -sourceAngle <= angle){
		p1 = intersection(cx, cy, arrowX, arrowY, x2, y1, x2, y2);
	}else if (angle > 0  && sourceAngle < Math.PI - angle){
		p1 = intersection(cx, cy, arrowX, arrowY, x1, y2, x2, y2);
	}else if (angle < 0  && -sourceAngle > -Math.PI - angle){
		p1 = intersection(cx, cy, arrowX, arrowY, x1, y1, x2, y1);
	}else{
		p1 = intersection(cx, cy, arrowX, arrowY, x1, y1, x1, y2);
	}
	context.beginPath();
	drawArrow(context, p1.x, p1.y, arrowX, arrowY);
	context.stroke();
}

//math
function cropPercent(value, size){
	value = ("" + value).trim();
	if (value.indexOf("%") >= 0)
		value = value.substring(0, value.length - 1).trim();
	return parseFloat(value) * size / 100;
}

function drawArrows(canvasId){
	var canvas = document.getElementById(canvasId);
	var context = canvas.getContext("2d");
	context.clearRect(0, 0, canvas.width, canvas.height);
	context.lineWidth = 5;
	context.strokeStyle = "rgba(243, 111, 33, 0.55)";
	//get elements
	for (var r = 0; r < result.length; r++){
		if (!result[r].target)
			continue;
		var source = document.getElementById(result[r].source);
		var target = document.getElementById(result[r].target).parentNode;
		var sx1 = cropPercent(source.style.left, canvas.width);
		var sy1 = cropPercent(source.style.top, canvas.height);
		var sw = cropPercent(source.style.width, canvas.width);
		var sh = cropPercent(source.style.height, canvas.height);
		var sx2 = sx1 + sw;
		var sy2 = sy1 + sh;
		var cx1 = sx1 + sw / 2;
		var cy1 = sy1 + sh / 2;
		var tx1 = cropPercent(target.style.left, canvas.width);
		var ty1 = cropPercent(target.style.top, canvas.height);
		var tw = cropPercent(target.style.width, canvas.width);
		var th = cropPercent(target.style.height, canvas.height);
		var tx2 = tx1 + tw;
		var ty2 = ty1 + th;
		var cx2 = tx1 + tw / 2;
		var cy2 = ty1 + th / 2;
		var angle = Math.atan2(cy2 - cy1, cx2 - cx1);
		var PI_2 = Math.PI * 1 / 2;
		var p1;
		var p2;
		//calculate source intersection
		var sourceAngle = Math.atan2(sy2 - sy1, sx2 - sx1);
		if (sourceAngle >= angle && -sourceAngle <= angle){
			p1 = intersection(cx1, cy1, cx2, cy2, sx2, sy1, sx2, sy2);
		}else if (angle > 0  && sourceAngle < Math.PI - angle){
			p1 = intersection(cx1, cy1, cx2, cy2, sx1, sy2, sx2, sy2);
		}else if (angle < 0  && -sourceAngle > -Math.PI - angle){
			p1 = intersection(cx1, cy1, cx2, cy2, sx1, sy1, sx2, sy1);
		}else{
			p1 = intersection(cx1, cy1, cx2, cy2, sx1, sy1, sx1, sy2);
		}
		//calculate target intersection
		var targetAngle = Math.atan2(ty2 - ty1, tx2 - tx1);
		if (targetAngle >= angle && -targetAngle <= angle){
			p2 = intersection(cx1, cy1, cx2, cy2, tx1, ty1, tx1, ty2);
		}else if (angle > 0  && targetAngle < Math.PI - angle){
			p2 = intersection(cx2, cy2, cx1, cy1, tx1, ty1, tx2, ty1);
		}else if (angle < 0  && -targetAngle > -Math.PI - angle){
			p2 = intersection(cx2, cy2, cx1, cy1, tx1, ty2, tx2, ty2);
		}else{
			p2 = intersection(cx2, cy2, cx1, cy1, tx2, ty1, tx2, ty2);
		}
		context.beginPath();
		drawArrow(context, p1.x,p1.y, p2.x,p2.y);
		context.stroke();
	}
}

function drawArrow(context, x11,y11, x12, y12){
	var head = 10;	// length of head in pixels
	var dx1 = x12 - x11;
	var dy = y12 - y11;
	var angle = Math.atan2(dy,dx1);
	context.moveTo(x11, y11);
	context.lineTo(x12, y12);
	context.lineTo(x12 - head * Math.cos(angle - Math.PI/6), y12 - head * Math.sin(angle - Math.PI/6));
	context.moveTo(x12, y12);
	context.lineTo(x12 - head * Math.cos(angle + Math.PI/6), y12 - head * Math.sin(angle + Math.PI/6));
}

function intersection(x1, y1, x2, y2, x3, y3, x4, y4){
	var a1, a2, b1, b2, c1, c2;
	var r1, r2 , r3, r4;
	var denom, offset, num;
	a1 = y2 - y1;
	b1 = x1 - x2;
	c1 = (x2 * y1) - (x1 * y2);
	r3 = ((a1 * x3) + (b1 * y3) + c1);
	r4 = ((a1 * x4) + (b1 * y4) + c1);
	a2 = y4 - y3;
	b2 = x3 - x4;
	c2 = (x4 * y3) - (x3 * y4);
	r1 = (a2 * x1) + (b2 * y1) + c2;
	r2 = (a2 * x2) + (b2 * y2) + c2;
	denom = (a1 * b2) - (a2 * b1);
	if (denom < 0){ 
		offset = -denom / 2; 
	}else{
		offset = denom / 2 ;
	}
	var point = new Object();
	num = (b1 * c2) - (b2 * c1);
	if (num < 0){
		point.x = (num - offset) / denom;
	}else{
		point .x = (num + offset) / denom;
	}
	num = (a2 * c1) - (a1 * c2);
	if (num < 0){
		point .y = ( num - offset) / denom;
	}else{
		point .y = (num + offset) / denom;
	}
	return point;
}

function getElementOffset(element) {
	var x = 0;
	var y = 0;
	while (element && !isNaN(element.offsetLeft) && !isNaN(element.offsetTop)){
		x += element.offsetLeft - element.scrollLeft;
		y += element.offsetTop - element.scrollTop;
		element = element.offsetParent;
	}
	return {dx: x, dy: y};
}

/* reset params*/
function resetCheckBox(ids){
	for (var i = 0; i < ids.length; i++){
		document.getElementById(ids[i]).checked = null;
	}
}

function resetRadioButton(ids){
	for (var i = 0; i < ids.length; i++){
		document.getElementById(ids[i]).checked = null;
	}
}

function resetPickSpot(ids){
	for (var i = 0; i < ids.length; i++){
		var spot = document.getElementById(ids[i]);
		var className = spot.className;
		if (!className)
			continue;
		className = className.replace("exercise_interactive_area_selected", "exercise_interactive_area");
		spot.className = className;
	}
}

function resetValueInRange(id){
	var input = document.getElementById(id);
	input.value = '0';
}

function resetArrows(canvasId, startIds, endIds){
	for (var i = 0; i < endIds.length; i++){
		var box = document.getElementById(endIds[i]);
		var className = box.className;
		if (!className)
			continue;
		className = className.replace("exercise_area_good", "");
		className = className.replace("exercise_area_wrong", "");
		className = className.trim();
		box.className = className;
	}
	var tempResult = [];
	main: for (var r = 0; r < result.length; r++){
		for (var i = 0; i < startIds.length; i++){
			if (result[r].source === startIds[i]){	
				continue main;
			}
		}
		tempResult.push(result[r]);
	}
	result = tempResult;
	drawArrows("ppArrowsCanvas" + canvasId);
}

function resetMoveObject(canvasId, startIds, endIds){
	main: for (var i = 0; i < endIds.length; i++){
		var box = document.getElementById(endIds[i]);
		//clean borders
		var className = box.className;
		if (!className)
			continue;
		className = className.replace("exercise_area_good", "");
		className = className.replace("exercise_area_wrong", "");
		className = className.trim();
		box.className = className;
		//check if it contains objects
		var children = box.getElementsByTagName("div");
		children: for (var c = 0; c < children.length; c++){
			var child = children[c];
			if (!child.id)
				continue children;
			if (child.id.indexOf("source") > 0){
				var sourceId = child.id.replace("prim_", "");
				var source = document.getElementById(sourceId);
				child.parentNode.removeChild(child);
				source.appendChild(child);
			}
		}	
	}
}

function getFunctionParams(functionName){
	var functionParams = functionName.substring(functionName.indexOf("(") + 1, functionName.indexOf(")"));
	var currentValue = "";
	var result = [];
	parse(result, functionParams);
	return result;
}

function parse(container, text){
	for (var i = 0; i < text.length; i++){
		var c = text.charAt(i);
		if (c == '['){
			i++;
			c = text.charAt(i)
			var arrayContent = '';
			var ar = [];
			container.push(ar);
			while (c != ']'){
				arrayContent += c;
				i++;
				c = text.charAt(i);
			}
			parse(ar, arrayContent);
			i++;
		}else if (c == '\''){
			var currentValue = "";
			i++;
			while ((c = text.charAt(i)) != '\''){
				currentValue += c;
				i++;
			}
			container.push(currentValue);
		}else if (c >= '0' && c <= '9'){
			var currentValue = "";
			while (c >= '0' && c <= '9'){
				currentValue += c;
				i++;
				c = text.charAt(i);
			}
			container.push(currentValue);
		}
	}
}

function resetExercise(qId){
	//get type through the function
	var submitButton = document.getElementById("submitButton" + qId);
	attemps = 0;
	//true/false case
	if (!el){
		closeAlertDialog(qId);
		return;
	}
	//others
	var functionName = submitButton.getAttribute("onclick").toLowerCase();
	var params = getFunctionParams(functionName);
	if (functionName.indexOf("checkbox") >= 0){
		resetCheckBox(params[0]);
	}else if (functionName.indexOf("radiobutton") >= 0){
		resetRadioButton(params[0]);
	}else if (functionName.indexOf("pickspot") >= 0){
		resetPickSpot(params[0]);
	}else if (functionName.indexOf("arrows") >= 0){
		resetArrows(qId, params[0], params[1]);
	}else if (functionName.indexOf("moveobject") >= 0){
		resetMoveObject(qId, params[0], params[1]);
	}else if (functionName.indexOf("valueinrange") >= 0){
		resetValueInRange(params[2]);
	}else{
		//window.location.href = window.location.href;
		console.log("unknows function: " + functionName);
	} 
}