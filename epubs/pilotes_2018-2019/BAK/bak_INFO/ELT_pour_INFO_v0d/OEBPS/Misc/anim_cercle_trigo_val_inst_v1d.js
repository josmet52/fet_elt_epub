
// fonctions handling de l'animation
// ************************************************************************

function onResizeAction () {
	 // ajuster le canvas a la fenetre
	var w0 = parseInt(0.95*window.innerWidth);
	var h0 = parseInt(0.95*window.innerHeight);
	var rw = w0 / w1 ;
	var rh = h0 / h1 ;
	var r_scale_factor = 1; 
	var r_scale;
	
	if (rw < rh) {
		r_scale = rw*r_scale_factor;
		if (r_scale*h1 > h0){
			r_scale = rh*r_scale_factor;
		}
	} else {
		r_scale = rh*r_scale_factor;
		if (r_scale*w1 > w0){
			r_scale = rw*r_scale_factor;
		}
	}
	r_width = w1*r_scale;
	r_height = h1*r_scale;

// dimensions de reference
	r_base = parseInt(r_height);
	r_margin = parseInt(r_base/28);

// dimension des éléments
	r_zone = parseInt(r_base/2);
	r_label = parseInt(r_zone - 1*r_margin);
	r_axe = parseInt(r_zone - 2*r_margin);
	r_circle = parseInt(r_zone - 3*r_margin);
	l_width = (r_zone/200);
	grad_len = parseInt(r_zone/50);
	letter_height = parseInt(l_width*12);
	letter_style = letter_height + "px Arial";
	
	canvas_element.height = r_height;
	canvas_element.width = r_width;
	RefreshGraph(ctx, r_zone, r_label, r_axe, r_circle, l_width, grad_len, letter_height, letter_style, ph_deg);
	// debugPrint0("w0="+w0, "w1="+w1, "rw="+rw.toFixed(2), "h0="+h0, "h1="+h1, "rh="+rh.toFixed(2), "r_scale="+r_scale.toFixed(2));
	// debugPrint("r_base="+r_base, "r_margin="+r_margin,"r_zone="+r_zone, "r_label="+r_label, "r_axe="+r_axe, "r_circle="+r_circle, "l_width="+l_width, "grad_len="+grad_len, "letter_height="+letter_height, letter_style, ph_deg);
}

function RefreshGraph(ctx, r_zone, r_label, r_axe, r_circle, l_width, grad_len, letter_height, letter_style, ph_deg){
	// onResizeAction ();
	drawZone(ctx, r_zone);
	drawCircle(ctx, r_zone, r_label, r_axe, r_circle, l_width, grad_len, letter_height, letter_style);
	draw_sinus(ctx, r_zone, r_label, r_axe, r_circle, l_width, grad_len, letter_height, letter_style, ph_deg);
	draw_dot_line(ctx, r_zone, r_circle, grad_len, ph_deg);
	drawVecteur(ctx, r_zone, r_circle, grad_len, ph_deg);
	if (!show_tension) {
		document.getElementById("txt_tension").style.display = "none";
	} else {
		document.getElementById("txt_tension").style.display = "";
	}
	if (!show_sin) {
		document.getElementById("txt_sin").style.display = "none";
	} else {
		document.getElementById("txt_sin").style.display = "";
	}
	if (!show_cos) {
		document.getElementById("txt_cos").style.display = "none";
	} else {
		document.getElementById("txt_cos").style.display = "";
	}
	if (!show_angle) {
		document.getElementById("txt_deg").style.display = "none";
	} else {
		document.getElementById("txt_deg").style.display = "";
	}

	showValues(document, r_circle, ph_deg);
}

// fonctions de l'animation du cercle trigonometrique
// ************************************************************************

function drawZone(ctx, r_zone){
	
	ctx.lineWidth = l_width;
	// effacer tout
	ctx.translate(0, 0);
	ctx.beginPath();
	ctx.fillStyle = fill_circle_color; 
	ctx.fillRect(0, 0, 2*r_zone, 2.1*r_zone);
	ctx.fill();
	ctx.stroke();
	
	ctx.beginPath();
	ctx.fillStyle = fill_box_color; 
	ctx.fillRect(2*r_zone, 0, f_dim*r_zone, 2*r_zone);
	ctx.fill();
	
	ctx.beginPath();
	ctx.strokeStyle = axe_line_color; 
	ctx.rect(2*r_zone, 0, f_dim*r_zone, 2*r_zone);
	ctx.stroke();
	
}

function drawCircle(ctx, r_zone, r_label, r_axe, r_circle, l_width, grad_len, letter_height, letter_style){
	
	var x_center = r_zone;
	var y_center = r_zone; 
	// dessiner le cercle
	// coordonnées du centre du cercle
	ctx.translate(x_center, y_center);
	ctx.beginPath();
	ctx.fillStyle = fill_box_color; //fill_circle_color; 
	ctx.strokeStyle = axe_line_color; 
	ctx.arc(0, 0, r_circle, 0, 2*Math.PI);
	// dessiner les axes
	drawArrow(ctx, 0, 0 , -r_axe, 0);
	drawArrow(ctx, 0, 0 , r_axe, 0);
	drawArrow(ctx, 0, 0 , 0, -r_axe);
	drawArrow(ctx, 0, 0 , 0, r_axe);
	// incrire les labels
	ctx.font =  letter_style;
	ctx.textAlign = "center";
	ctx.strokeText("x", r_label, +letter_height/4);
	ctx.strokeText("-x", -r_label, +letter_height/4);
	ctx.strokeText("y", 0, -r_label);
	ctx.strokeText("-y", 0, r_label);
	ctx.fill();
	// dessiner les graduations
	nbre_grad = 4;
	for (i=0; i<nbre_grad; i++){
		v = i+1;
		p = r_circle / nbre_grad * v;
		g = grad_len;
		//axe des abcisses
		ctx.moveTo(p,-g);
		ctx.lineTo(p,g);
		ctx.moveTo(-p,-g);
		ctx.lineTo(-p,g);
		// label des abcisses
		if (show_label){
			ctx.textAlign = "center";
			ctx.strokeText((v/nbre_grad), p, 4*grad_len);
			ctx.strokeText((-v/nbre_grad), -p, 4*grad_len);
		}
		//axe des ordonnees
		ctx.moveTo(-g,p);
		ctx.lineTo(g,p);
		ctx.moveTo(-g,-p);
		ctx.lineTo(g,-p);
		if (show_label){
			ctx.textAlign = "left";
			ctx.strokeText((-p, v/nbre_grad), 2*grad_len, p+letter_height/4);
			ctx.strokeText((p, v/nbre_grad), 2*grad_len, -p+letter_height/4);
		}
	}
	ctx.stroke();
	ctx.translate(-x_center, -y_center);
}

function draw_sinus(ctx, r_zone, r_label, r_axe, r_circle, l_width, grad_len, letter_height, letter_style) {
	
	var r_margin = parseInt(r_zone/4);
	
	var x_zone = parseInt(r_zone * f_dim);
	var x_label = parseInt(r_label * f_dim);
	var x_axe = parseInt(r_axe * f_dim);
	var x_curve = parseInt(r_circle * f_dim);
	
	var y_zone = r_zone;
	var y_label = r_label;
	var y_axe = r_axe;
	var y_curve = r_circle;
	
	var x0_box = 2*r_zone;
	var y0_box = 0;
	var x1_box = 4*r_zone ;
	var y1_box = 2*r_zone;
	
	var x0_graph =  x0_box + r_margin;
	var y0_graph = -y0_box + r_zone;
	var x_min = 0;
	var y_min = 0;

	var i;

	// debugPrint1("r_margin="+r_margin, "xZone="+x_zone, "x_label="+x_label, "x_axe="+x_axe, "x_curve="+x_curve, "x0_box="+x0_box, "x1_box="+x1_box);
	
	// draw axes
	ctx.translate(x0_graph, y0_graph);
	ctx.beginPath();
	ctx.lineWidth = l_width;
	ctx.strokeStyle = axe_line_color; 
	ctx.textStyle = label_text_color;
	drawArrow(ctx, 0, 0, x_axe, 0);
	drawArrow(ctx, 0, 0, 0, -y_axe);
	drawArrow(ctx, 0, 0, 0, y_axe);

	// draw x graduations 
	ctx.font = letter_style;
	ctx.textAlign = "center";
	var nbre_grad = 8;
	for (i = 0; i<nbre_grad+1; i++) {
		var x_grad = (i) * x_curve / nbre_grad;
		ctx.moveTo(x_grad, -grad_len);
		ctx.lineTo(x_grad, grad_len);
		if (show_label){
			ctx.strokeText(45 * i, x_grad, 4*grad_len);
		}
		if (show_grid){
			ctx.moveTo(x_grad, -y_curve);
			ctx.lineTo(x_grad, y_curve);
		}
	}
	ctx.moveTo(0, 0);
	ctx.stroke();

	// draw y graduations 
	ctx.beginPath();
	ctx.font = letter_style;
	ctx.textAlign = "right";
	for (i = -4; i != 5; i++) {
		var y_grad = i * y_curve / 4;
		ctx.moveTo(-grad_len, y_grad);
		ctx.lineTo(grad_len, y_grad);
		if (show_label){
			if (show_tension) {
				ctx.strokeText((-0.25 * i * 230 * Math.sqrt(2)).toPrecision(3), - 2*grad_len, y_grad + grad_len / 2);
			} else {
				ctx.strokeText(-0.25 * i, - 2*grad_len, y_grad + grad_len / 2);
			}
		}
		if (show_grid){
			ctx.moveTo(0, y_grad);
			ctx.lineTo(x_curve, y_grad);
		}
	}
	ctx.moveTo(0, 0);
	ctx.stroke();
	
	// draw labels
	ctx.beginPath();
	ctx.font = letter_style;
	ctx.textAlign = "center";
	// axe des ordonnées
	ctx.textAlign = "right";
	ctx.strokeText("i", 0, -y_label);
	// ctx.strokeText("-i", 0, y_label);
	// axe des abcisses
	ctx.strokeText("φ", x_axe, 4*grad_len)

	// draw sinus
	var x_old = 0.0;
	var y_old = 0.0;
	var x_new = 0.0;
	var y_new = 0.0;
	var ph = 360;
	ctx.beginPath();
	ctx.lineWidth = l_width ;
	ctx.strokeStyle = sin_color;
	for (i = 0; i < ph; i++) {
		x_new = i * x_curve / 360;
		var y_rad = i * Math.PI / 180;
		var y_sin = -Math.sin(y_rad);
		y_new = y_sin * y_curve;
		ctx.moveTo(x_old, y_old);
		ctx.lineTo(x_new, y_new);
		x_old = x_new;
		y_old = y_new;
	}
	ctx.moveTo(0, 0);
	ctx.stroke();
	
	ctx.translate(-x0_graph, -y0_graph);
}
	
function draw_dot_line(ctx, r_zone, r_circle, grad_len, ph_deg){

	var r_margin = r_zone/4;
	
	var x0_graph =  2*r_zone + r_margin;
	var y0_graph =  r_zone;
	var x0_circle = x0_graph - r_zone - r_margin;
	
	var x_curve = r_circle * f_dim;
	var y_curve = r_circle;

	// get coordinates
	var ph_rad = ph_deg * Math.PI / 180;
	x_new = ph_deg * x_curve / 360;
	var y_sin = -Math.sin(ph_rad);
	var x_cos = -Math.cos(ph_rad);
	y_new = y_sin * y_curve;
	
	// draw dot on curve
	ctx.translate(x0_graph, y0_graph);
	ctx.beginPath();
	ctx.fillStyle = line_color;
	ctx.strokeStyle = line_color;
	ctx.arc(x_new, y_new, grad_len, 0, 2 * Math.PI);
	ctx.fill();
	
	// draw sin cos lines
	ctx.lineWidth = l_width;
	ctx.setLineDash([3]);
	ctx.moveTo(x_new, 0);
	ctx.lineTo(x_new, y_new);
	ctx.moveTo(x_new, y_new);
	var x_val;
	if (x_cos > 0){
		x_val = -r_margin -r_zone -x_cos * r_circle;
	} else {
		x_val = -r_margin -r_zone;
	}
	ctx.lineTo(x_val , y_new);
	ctx.moveTo(-r_margin -r_zone -x_cos * r_circle , y_new);
	ctx.lineTo(-r_margin -r_zone -x_cos * r_circle , 0);
	ctx.stroke();
	ctx.setLineDash([]);
	
	//draw dot on circle
	ctx.moveTo(-r_margin -r_zone- x_cos * r_circle , y_new);
	ctx.arc(-r_margin -r_zone -x_cos * r_circle , y_new, grad_len, 0, 2 * Math.PI);
	ctx.fill();
	
	
	ctx.moveTo(0, 0);
	ctx.translate(-x0_graph, -y0_graph);
}
	
function drawVecteur(ctx, r_zone, r_circle, grad_len, ph_deg){
	
	var x_center = r_zone;
	var y_center = r_zone; 
	var r_measure = r_circle/3;

	// get coordinates
	var ph_rad = ph_deg * Math.PI / 180;
	var y_sin = -Math.sin(ph_rad);
	if (Math.abs(y_sin) < 0.001){
		y_sin = 0;
	}
	var x_cos = Math.cos(ph_rad);
	if (Math.abs(x_cos) < 0.001){
		x_cos = 0;
	}
	
	x_new = x_cos * r_circle;
	y_new = y_sin * r_circle;

	// coordonnées du centre du cercle
	ctx.translate(x_center, y_center);
	
	ctx.lineWidth = 2*l_width;
	ctx.strokeStyle = line_color;
	ctx.beginPath();
	ctx.moveTo(0, 0);
	//draw the vector
	drawArrow(ctx, 0,0, x_new, y_new)
	ctx.stroke();
	//draw the sin and cos line
	ctx.lineWidth = 1*l_width;
	ctx.beginPath();
	// draw the angle measure
	ctx.strokeStyle = line_color;
	if (ph_rad != 0) {
		ctx.arc(0, 0, r_measure, 0, 2*Math.PI-ph_rad, true);
	}
	// draw the arrow for the angle measure
	// ctx.moveTo(Math.cos(ph_rad)*r_measure, -Math.sin(ph_rad)*r_measure);
	// var angle_arrow = ph_rad - Math.PI/6;
	// ctx.lineTo(Math.sin(angle_arrow),-Math.sin(ph_rad)*r_measure-10);
	
	// ctx.moveTo(Math.cos(ph_rad)*r_measure, -Math.sin(ph_rad)*r_measure);
	// ctx.lineTo(Math.cos(angle_arrow),Math.sin(ph_rad)*r_measure+10);
	
	ctx.arc(Math.cos(ph_rad)*r_measure, -Math.sin(ph_rad)*r_measure, grad_len, 0, 2*Math.PI, true);
	
	
	ctx.stroke();
	// ctx.beginPath();
	// ctx.strokeStyle = "yellow";
	// ctx.arc(0, 0, r_circle/3, ph_rad, 0, false);
	// ctx.stroke();
	
	
	// draw cos arrow
	ctx.beginPath();
	ctx.lineWidth = 3*l_width;
	ctx.strokeStyle = cos_color;
	if ((ph_deg != 90) && (ph_deg != 270)){
		drawArrow(ctx, 0,0, x_new, 0);
	}
	ctx.stroke();
	// draw sin arrow
	ctx.beginPath();
	ctx.strokeStyle = sin_color;
	if ((ph_deg != 0) && (ph_deg != 180) && (ph_deg != 360)){
		drawArrow(ctx, 0,0, 0, y_new);
	}
	ctx.stroke();
	ctx.translate(-x_center, -y_center);
}
	
function showValues(document, r_circle, ph_deg) {
	// get coordinates
	var ph_rad = ph_deg * Math.PI / 180;
	var y_sin = -Math.sin(ph_rad);
	if (Math.abs(y_sin) < 0.001){
		y_sin = 0;
	}
	var x_cos = Math.cos(ph_rad);
	if (Math.abs(x_cos) < 0.001){
		x_cos = 0;
	}
	document.getElementById("txt_deg").innerHTML = "angle = " + ph_deg.toPrecision(3)+ "˚";
	document.getElementById("txt_sin").innerHTML = "sin = " + -y_sin.toPrecision(3);
	document.getElementById("txt_cos").innerHTML = "cos = " + x_cos.toPrecision(3);
	document.getElementById("txt_tension").innerHTML = "U = " + (-y_sin*230*Math.sqrt(2)).toPrecision(3) +" V";
}

// fonctions boutons et checkbox
// ************************************************************************

// lancer la rotation automatique
function btnRun() {
	if (!anim_running) {
		idVector = setInterval(animateVector, sleep_time);
		anim_running = true;
	} else {
		stop_asked = true;
	}
}
// arreter la rotation automatique
function btnStop() {
	if (anim_running) {
		stop_asked = true;
	}
}
// fonction appelee par runMotor()
function animateVector() {
	RefreshGraph(ctx, r_zone, r_label, r_axe, r_circle, l_width, grad_len, letter_height, letter_style, ph_deg)
	ph_deg = (ph_deg+ph_inc)%360;
	if ((ph_deg%5 == 0) && stop_asked) {
		clearInterval(idVector);
		anim_running = false;
		stop_asked = false;
	}
}
// faire un pas dans le sens positif
function btnStepPlus() {
	if (!anim_running) {
		if (ph_deg == 360) {
			ph_deg = 0;
		} else {
			ph_deg = ph_deg + 1;
		}
		RefreshGraph(ctx, r_zone, r_label, r_axe, r_circle, l_width, grad_len, letter_height, letter_style, ph_deg);
	}
}
// faire un pas dans le sens positif
function btnStepPlusPlus() {
	if (!anim_running) {
		if (ph_deg == 360) {
			ph_deg = 0;
		} else {
			ph_deg = ph_deg + 5;
		}
		RefreshGraph(ctx, r_zone, r_label, r_axe, r_circle, l_width, grad_len, letter_height, letter_style, ph_deg);
	}
}
// faire un pas dans le sens negatif
function btnStepMoins() {
	if (!anim_running) {
		ph_deg = ph_deg - 1;
		if (ph_deg < 0) {
			ph_deg = 360;
		}
		RefreshGraph(ctx, r_zone, r_label, r_axe, r_circle, l_width, grad_len, letter_height, letter_style, ph_deg);
	}
}
// faire un pas dans le sens negatif
function btnStepMoinsMoins() {
	if (!anim_running) {
		ph_deg = ph_deg - 5;
		if (ph_deg < 0) {
			ph_deg = 360;
		}
		RefreshGraph(ctx, r_zone, r_label, r_axe, r_circle, l_width, grad_len, letter_height, letter_style, ph_deg);
	}
}
// afficher les etiquettes O/M 
function optEtiquetteYesNo(value){
    if (value) {
        show_label = true;
    } else {
        show_label = false;
    }
	RefreshGraph(ctx, r_zone, r_label, r_axe, r_circle, l_width, grad_len, letter_height, letter_style, ph_deg);
}
	
// afficher les etiquettes O/M 
function optTensionYesNo(value){
    if (value) {
        show_tension = true;
    } else {
        show_tension = false;
    }
	RefreshGraph(ctx, r_zone, r_label, r_axe, r_circle, l_width, grad_len, letter_height, letter_style, ph_deg);
}
// aficher la grille O/N
function optGrilleYesNo(value){
   if (value) {
        show_grid = true;
    } else {
        show_grid = false;
    }
	RefreshGraph(ctx, r_zone, r_label, r_axe, r_circle, l_width, grad_len, letter_height, letter_style, ph_deg);
}

// fonctions utilitaires
// ************************************************************************

function drawArrow(ctx, fromx, fromy, tox, toy) {
	var headlen = 10; // length of head in pixels
	var angle = Math.atan2(toy - fromy, tox - fromx);
	ctx.moveTo(fromx, fromy);
	ctx.lineTo(tox, toy);
	ctx.lineTo(tox - headlen * Math.cos(angle - Math.PI / 6), toy - headlen * Math.sin(angle - Math.PI / 6));
	ctx.moveTo(tox, toy);
	ctx.lineTo(tox - headlen * Math.cos(angle + Math.PI / 6), toy - headlen * Math.sin(angle + Math.PI / 6));
}
