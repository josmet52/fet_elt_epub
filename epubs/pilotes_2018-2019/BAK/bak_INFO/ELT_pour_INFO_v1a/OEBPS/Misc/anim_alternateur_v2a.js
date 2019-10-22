// ************************************************************************
// fonctions dessin de l'animation
// ************************************************************************

function onResizeAction () {
    
	
	 // ajuster le canvas a la fenetre
    var w0 = parseInt(0.95 * window.innerWidth);
    var h0 = parseInt(0.95*window.innerHeight);
    var rw = w0 / w1 ;
    var rh = h0 / h1 ;
    var r_scale_factor = 1.03;

	if (rw < rh) {
		rf = rw*r_scale_factor;
		if (rf*h1 > h0){
			rf = rh*r_scale_factor;
		}
	} else {
		rf = rh*r_scale_factor;
		if (rf*w1 > w0){
			rf = rw*r_scale_factor;
		}
	}
	canvas_element.width = w1 * rf; // ajuster la largeur du canvas à la fenetre
	canvas_element.height = h1 * rf; // ajuster la hauteur du canvas à la fenetre

	Rr = canvas_element.height / 2; // si height = 400 alors R = 200
	R = canvas_element.height / 2.22; // si height = 400 alors R = 180
	Rx = canvas_element.height / 1.54; // si height = 400 alors R = 260
	l_width = canvas_element.height / 400;
	gradLen = canvas_element.height / 100;

	 // initialisation dimensions et décalage du graphqie
	Ymin = 0; 
	Ymax = R * 0.9; 
	Xmin = Rx;
	Xmax = 3.7 * R;
	Xlen = Xmax - Xmin; // longueur de l'axe des x
	
	// var Rx = 0
	s = 0.35 * R; // epaisseur du stator
	r = R - s / 2; // rayon moyen du stator
	c = s / 2; // cote de l'encoche
	w = 0.35 * c; // diametre du fil
					
	refreshGraph();
}

function refreshGraph(){
	if (monophase_YN){
		txt_ph2.style.display = "none";
		txt_ph3.style.display = "none";
		// btn_mono.style.display = "none";
	} else {
		txt_ph2.style.display = "inline-block";
		txt_ph3.style.display = "inline-block";
		// btn_mono.style.display = "inline";
	}
	
	ctx.translate(R + canvas_element.height / 20, R + canvas_element.height / 20);
	drawStator(ctx, r, s, p, c, w); // dessiner le stator
	drawRotor(ctx, R, s, p); // dessiner le rotor
	draw_sinus(ctx, Rr, R, p); // dessiner la courbe sinusoidale
	ctx.translate(-R - canvas_element.height / 20, -R - canvas_element.height / 20);
}

function drawStator(ctx, r, s, p, c, w) {
    // dessiner le stator

    // les toles
    var p_rad = p / 180 * Math.PI;
    ctx.beginPath();
    ctx.arc(0, 0, r, 0, 2 * Math.PI);
    ctx.lineWidth = s;
    ctx.strokeStyle = "gray";
    ctx.stroke();
    // la ligne noire extérieure
    ctx.beginPath();
    ctx.arc(0, 0, R, 0, 2 * Math.PI);
    ctx.lineWidth = l_width;
    ctx.strokeStyle = "black";
    ctx.stroke();
    // la ligne noire intérieure
    ctx.beginPath();
    ctx.arc(0, 0, R - s, 0, 2 * Math.PI);
    ctx.lineWidth = l_width;
    ctx.strokeStyle = "black";
    ctx.fillStyle = "green";
    ctx.stroke();

    phase_delta = 15;
    //dessiner les encoches et les fils phase 1
    phase_deg = 0;
    phase_deg_1 = phase_deg + 90;
    drawWire(ctx, r, s, phase_deg_1 - phase_delta, c, w, phase_deg, p);
    drawWire(ctx, r, s, phase_deg_1, c, w, phase_deg, p);
    drawWire(ctx, r, s, phase_deg_1 + phase_delta, c, w, phase_deg, p);
    drawWire(ctx, r, s, phase_deg_1 - phase_delta + 180, c, w, phase_deg, p);
    drawWire(ctx, r, s, phase_deg_1 + 180, c, w, phase_deg, p);
    drawWire(ctx, r, s, phase_deg_1 + phase_delta + 180, c, w, phase_deg, p);

    if (!monophase_YN) {
        //dessiner les encoches et les fils phase 2
        phase_deg = 120;
        phase_deg_1 = phase_deg + 90;
        drawWire(ctx, r, s, phase_deg_1 - phase_delta, c, w, phase_deg, p);
        drawWire(ctx, r, s, phase_deg_1, c, w, phase_deg, p);
        drawWire(ctx, r, s, phase_deg_1 + phase_delta, c, w, phase_deg, p);
        drawWire(ctx, r, s, phase_deg_1 - phase_delta + 180, c, w, phase_deg, p);
        drawWire(ctx, r, s, phase_deg_1 + 180, c, w, phase_deg, p);
        drawWire(ctx, r, s, phase_deg_1 + phase_delta + 180, c, w, phase_deg, p);

        //dessiner les encoches et les fils phase 3
        phase_deg = 240;
        phase_deg_1 = phase_deg + 90;
        drawWire(ctx, r, s, phase_deg_1 - phase_delta, c, w, phase_deg, p);
        drawWire(ctx, r, s, phase_deg_1, c, w, phase_deg, p);
        drawWire(ctx, r, s, phase_deg_1 + phase_delta, c, w, phase_deg, p);
        drawWire(ctx, r, s, phase_deg_1 - phase_delta + 180, c, w, phase_deg, p);
        drawWire(ctx, r, s, phase_deg_1 + 180, c, w, phase_deg, p);
        drawWire(ctx, r, s, phase_deg_1 + phase_delta + 180, c, w, phase_deg, p);
    }
}

function drawWire(ctx, r, s, p, c, w, phase_deg, ph) {
    // dessiner les fils
    var p_rad = p / 180 * Math.PI; // l'angle en radians
    // dessiner l'encoche
    var c1 = R - s - c / 8;
    ctx.rotate(p_rad);
    ctx.translate(c1, -c / 2);
    ctx.beginPath();
    ctx.strokeStyle = "black";
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, c, c);
    ctx.lineWidth = l_width;
    ctx.strokeRect(0, 0, c, c);
    ctx.translate(-c1, c / 2);
    ctx.rotate(-p_rad);

    // dessiner le fil
    var c2 = R - s + w;
    ctx.rotate(p_rad);
    ctx.translate(c2, 0);
    ctx.beginPath();
    ctx.strokeStyle = "black";
    ctx.fillStyle = "#ffe4b5";
    ctx.arc(0, 0, w, 0, 2 * Math.PI);
    ctx.lineWidth = l_width;
    ctx.fill();
    ctx.stroke();
    ctx.translate(-c2, 0);
    ctx.rotate(-p_rad);

    if (phase_deg == 0) {
        ctx.fillStyle = ph1_color; // OrangeRed
        ctx.strokeStyle = ph1_color;
        p_rot = p_rad;
        dp = 0;
    } else if (phase_deg == 120) {
        ctx.fillStyle = ph2_color; // LightSkyBlue
        ctx.strokeStyle = ph2_color;
        p_rot = p_rad;
        dp = 240;
    } else if (phase_deg == 240) {
        ctx.fillStyle = ph3_color; // LimeGreen
        ctx.strokeStyle = ph3_color;
        p_rot = p_rad;
        dp = 120;
    }
    // show the current phase 1
    ctx.rotate(p_rot);
    ctx.translate(c2, 0);
    ctx.beginPath();
    ctx.lineWidth = l_width * 3;

    wf = w * Math.abs(Math.sin((ph + dp) / 180 * Math.PI));

    if (((p + dp) % 360) < 180) {
        if (((ph + dp) % 360) < 180) {
            ctx.moveTo(-wf / 2, -wf / 2);
            ctx.lineTo(wf / 2, wf / 2);
            ctx.moveTo(wf / 2, -wf / 2);
            ctx.lineTo(-wf / 2, wf / 2);
        } else {
            ctx.arc(0, 0, wf * 0.5, 0, 2 * Math.PI);
        }
    } else {
        if (((ph + dp) % 360) >= 180) {
            ctx.moveTo(-wf / 2, -wf / 2);
            ctx.lineTo(wf / 2, wf / 2);
            ctx.moveTo(wf / 2, -wf / 2);
            ctx.lineTo(-wf / 2, wf / 2);
        } else {
            ctx.arc(0, 0, wf * 0.5, 0, 2 * Math.PI);
        }
    }
    ctx.fill();
    ctx.stroke();
    ctx.translate(-c2, 0);
    ctx.rotate(-p_rot); //  - phase_deg/180*Math.PI
}

function drawRotor(ctx, R, s, p) {
    // dessiner le rotor
    ctx.translate(0, 0, 0, 0);
    // effacer le rotor
    ctx.beginPath();
    ctx.fillStyle = "white";
    ctx.lineWidth = l_width;
    ctx.arc(0, 0, (R - s) - 2, 0, 2 * Math.PI);
    ctx.fill();

    //dessiner le rotor
    var stator_angle_rad = p / 180 * Math.PI; // angle en radians
    var stator_len = R - 1.2 * s; // longueur d'un demi rotor
    var stator_width = s; // epaisseur du rotor idem epaisseur du stator
    // taille et police des caracteres N et S
    var letter_height = (l_width * 35).toFixed();
    ctx.font = letter_height + "px Verdana";

    // le pôle sud
    ctx.rotate(stator_angle_rad + Math.PI);
    ctx.translate(0, -stator_width / 2);
    ctx.beginPath();
    ctx.fillStyle = "#00cc00"; // vert clair
    ctx.fillRect(0, 0, stator_len, stator_width);
    ctx.fillStyle = "black";
    ctx.fillText("S", stator_len/2 , stator_width - (stator_width - letter_height * 1.25));
    ctx.fill();
    ctx.rect(0, 0, stator_len, stator_width);
    ctx.strokeStyle = "black";
    ctx.stroke();
    ctx.translate(0, stator_width / 2);
    ctx.rotate(-stator_angle_rad - Math.PI);

    // le pôle nord
    ctx.rotate(stator_angle_rad);
    ctx.translate(0, -stator_width / 2);
    ctx.beginPath();
    ctx.fillStyle = "red"; // rouge
    ctx.strokeStyle = "black";
    ctx.fillRect(0, 0, stator_len, stator_width);
    ctx.fillStyle = "black";
    ctx.fillText("N", stator_len/2, stator_width - (stator_width - letter_height * 1.25));
    ctx.fill();
    ctx.rect(0, 0, stator_len, stator_width);
    ctx.strokeStyle = "black";
    ctx.stroke();
    ctx.translate(0, stator_width / 2);
    ctx.rotate(-stator_angle_rad);

    // dessiner le centre
    ctx.beginPath();
    var line_long = R / 10;
    ctx.strokeStyle = "black";
    ctx.lineWidth = l_width;
    ctx.moveTo(-line_long / 2, 0);
    ctx.lineTo(line_long / 2, 0);
    ctx.moveTo(0, -line_long / 2);
    ctx.lineTo(0, line_long / 2);
    ctx.moveTo(0, 0);
    ctx.arc(0, 0, R / 30, 0, 2 * Math.PI);
    ctx.stroke();
}

function draw_sinus(ctx, Rr, R, ph1) {

    var ph2 = (ph1 % 360).toFixed();
    ph = 360;
    document.getElementById("txt_deg_id").innerHTML = "φ = " + ph2 + "˚";

    // draw box
    ctx.translate(Rr * 1.1, -R);
    ctx.beginPath();
    ctx.strokeStyle = "black";
    ctx.fillStyle = "#ffffe6"; // jaune clair
    ctx.fillRect(0, 0, 4.2 * R, 2 * R);
    ctx.lineWidth = l_width / 2;
    ctx.strokeRect(0, 0, 4.2 * R, 2 * R);
    ctx.translate(-Rr * 1.1, R);

    //draw axes
    ctx.translate(Xmin, -Ymin);
    ctx.beginPath();
    ctx.moveTo(0, 0);
    draw_arrow(ctx, 0, 0, 1.05 * Xmax, Ymin);
    ctx.moveTo(0, 0);
    draw_arrow(ctx, 0, 0, 0, -Ymax * 1.05);
    ctx.moveTo(0, 0);
    draw_arrow(ctx, 0, 0, 0, Ymax * 1.05);
    ctx.moveTo(0, 0);
    ctx.stroke();
    ctx.translate(-Xmin, Ymin);

    //draw x graduations 
    ctx.translate(Xmin, -Ymin);
    ctx.beginPath();
    ctx.lineWidth = l_width / 2;
    var letter_height = l_width * 12;
    var letter_style = "normal " + letter_height + "px San serif";
    ctx.font = letter_style;
    ctx.textAlign = "center";
	ctx.textStyle = label_text_color;
	ctx.fillStyle = label_text_color;
    for (var i = 1; i != 9; i++) {
        var Xgrad = i * (Xmin + Xlen) / 8;
        ctx.moveTo(Xgrad, -gradLen);
        ctx.lineTo(Xgrad, gradLen);
		if (valeurs_YN) {
			ctx.fillText(45 * i, Xgrad, 4 * gradLen);
		}
    }
    Xgrad = 8.3 * (Xmin + Xlen) / 8;
	if (valeurs_YN) {
		ctx.fillText("φ[º]", Xgrad, 5 * gradLen);
	}
	
    ctx.moveTo(0, 0);
    ctx.stroke();
    ctx.translate(-Xmin, Ymin);

    //draw y graduations 
    ctx.translate(Xmin, -Ymin);
    ctx.beginPath();
    ctx.lineWidth = l_width / 2;
    letter_height = (l_width * 12).toFixed();
    letter_style = "normal " + letter_height + "px San serif";
    ctx.font = letter_style;
    ctx.textAlign = "center";
    for (i = -4; i != 5; i++) {
        var Ygrad = i * Ymax / 4;
        ctx.moveTo(-gradLen, Ygrad);
        ctx.lineTo(gradLen, Ygrad);
	ctx.textStyle = label_text_color;
	ctx.fillStyle = label_text_color;
		if (valeurs_YN) {
			ctx.fillText(-0.25 * i * u_crete, -5 * gradLen, Ygrad + gradLen / 2);
		}
    }
	Ygrad = -4 * Ymax / 4;
	ctx.fillText("U[V]", +6 * gradLen, (Ygrad - gradLen ));
				
    ctx.moveTo(0, 0);
    ctx.stroke();
    ctx.translate(-Xmin, Ymin);

    // draw sinus phase 1
    ctx.translate(Xmin, -Ymin);
    var Xold = 0.0;
    var Yold = 0.0;
    var Xnew = 0.0;
    var Ynew = 0.0;
    ctx.beginPath();
    ctx.lineWidth = l_width * 1;
    //phase 1
    ctx.strokeStyle = ph1_color;
    for (i = 0; i < ph; i++) {
        // console.log(i, ph, i-ph, Math.sign(i-ph));
        Xnew = i * (Xmin + Xlen) / 360;
        var Yrad = i * Math.PI / 180;
        var Ysin = -Math.sin(Yrad);
        Ynew = Ysin * Ymax;
        ctx.moveTo(Xold, Yold);
        ctx.lineTo(Xnew, Ynew);
        Xold = Xnew;
        Yold = Ynew;
    }
    ctx.stroke();
    if (!monophase_YN) {
        //phase 2
        ctx.moveTo(0, 0);
        Xold = 0;
        Yold = -Math.sin(2 / 3 * Math.PI) * Ymax;
        ctx.beginPath();
        ctx.lineWidth = l_width * 1;
        ctx.strokeStyle = ph3_color;
        for (i = 0; i < ph; i++) {
            // console.log(i, ph, i-ph, Math.sign(i-ph));
            Xnew = i * (Xmin + Xlen) / 360;
            Yrad = i * Math.PI / 180;
            Ysin = -Math.sin(Yrad + 2 / 3 * Math.PI);
            Ynew = Ysin * Ymax;
            ctx.moveTo(Xold, Yold);
            ctx.lineTo(Xnew, Ynew);
            Xold = Xnew;
            Yold = Ynew;
        }
        ctx.stroke();
        //phase 3
        ctx.moveTo(0, 0);
        Xold = 0;
        Yold = -Math.sin(4 / 3 * Math.PI) * Ymax;
        ctx.beginPath();
        ctx.lineWidth = l_width * 1;
        ctx.strokeStyle = ph2_color;
        for (i = 0; i < ph; i++) {
            // console.log(i, ph, i-ph, Math.sign(i-ph));
            Xnew = i * (Xmin + Xlen) / 360;
            Yrad = i * Math.PI / 180;
            Ysin = -Math.sin(Yrad + 4 / 3 * Math.PI);
            Ynew = Ysin * Ymax;
            ctx.moveTo(Xold, Yold);
            ctx.lineTo(Xnew, Ynew);
            Xold = Xnew;
            Yold = Ynew;
        }
        ctx.stroke();
        ctx.moveTo(0, 0);
		
        ctx.stroke();
		
    }
    ctx.translate(-Xmin, Ymin);

    // draw dots phase 1
    ctx.translate(Xmin, -Ymin);
    ctx.beginPath();
    ctx.fillStyle = ph1_color;
    Xnew = ph2 * (Xmin + Xlen) / 360;
    Yrad = ph2 * Math.PI / 180;
    Ysin = -Math.sin(Yrad);
    Ynew = Ysin * Ymax;
    ctx.arc(Xnew, Ynew, w / 2, 0, 2 * Math.PI);
    if (Math.abs(Ysin) < 0.001) {
        Ysin = 0;
    }
	var u_ph1 = u_crete * Ysin;
	
	document.getElementById("txt_ph1_id").innerHTML = "U=" + -(u_crete * Ysin).toPrecision(3)+ "V";
    ctx.fill();
    // draw_sin cos lines
    if (lines_YN) {
        ctx.strokeStyle = ph1_color;
        ctx.lineWidth = 1;
        ctx.setLineDash([3]);
        ctx.moveTo(Xnew, 0);
        ctx.lineTo(Xnew, Ynew);
        ctx.moveTo(Xnew, Ynew);
        ctx.lineTo(0, Ynew);
        ctx.fill();
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.moveTo(0, 0);
    }

    if (!monophase_YN) {
        // draw dots phase 2
        ctx.beginPath();
        ctx.fillStyle = ph3_color;
        Xnew = ph2 * (Xmin + Xlen) / 360;
        Yrad = ph2 * Math.PI / 180;
        Ysin = -Math.sin(Yrad + 2 / 3 * Math.PI);
        Ynew = Ysin * Ymax;
        ctx.arc(Xnew, Ynew, w / 2, 0, 2 * Math.PI);
        if (Math.abs(Ysin) < 0.001) {
            Ysin = 0;
        }
		var u_ph2 = u_crete * Ysin;
		
		document.getElementById("txt_ph3_id").innerHTML = "U=" + -(u_crete * Ysin).toPrecision(3)+ "V";
        ctx.fill();
        // draw_sin cos lines
        if (lines_YN) {
            ctx.strokeStyle = ph3_color;
            ctx.lineWidth = 1;
            ctx.setLineDash([3]);
            ctx.moveTo(Xnew, 0);
            ctx.lineTo(Xnew, Ynew);
            ctx.moveTo(Xnew, Ynew);
            ctx.lineTo(0, Ynew);
            ctx.fill();
            ctx.stroke();
            ctx.setLineDash([]);
            ctx.moveTo(0, 0);
        }

        // draw dots phase 3
        ctx.beginPath();
        ctx.fillStyle = ph2_color;
        Xnew = ph2 * (Xmin + Xlen) / 360;
        Yrad = ph2 * Math.PI / 180;
        Ysin = -Math.sin(Yrad + 4 / 3 * Math.PI);
        Ynew = Ysin * Ymax;
        ctx.arc(Xnew, Ynew, w / 2, 0, 2 * Math.PI);
        if (Math.abs(Ysin) < 0.001) {
            Ysin = 0;
        }
		var u_ph3 = u_crete * Ysin;
		
		 document.getElementById("txt_ph2_id").innerHTML = "U=" + -(u_crete * Ysin).toPrecision(3)+ "V";
        ctx.fill();
        // draw_sin cos lines
        if (lines_YN) {
            ctx.strokeStyle = ph2_color;
            ctx.lineWidth = 1;
            ctx.setLineDash([3]);
            ctx.moveTo(Xnew, 0);
            ctx.lineTo(Xnew, Ynew);
            ctx.moveTo(Xnew, Ynew);
            ctx.lineTo(0, Ynew);
            ctx.fill();
            ctx.stroke();
            ctx.setLineDash([]);
            ctx.moveTo(0, 0);
        }
    }
    ctx.translate(-Xmin, Ymin);

}

// ************************************************************************
// fonctions utilitaires
// ************************************************************************

// draw arrow lines
function draw_arrow(ctx, fromx, fromy, tox, toy) {
    const headlen = 10; // length of head in pixels
    var angle = Math.atan2(toy - fromy, tox - fromx);
    ctx.moveTo(fromx, fromy);
    ctx.lineTo(tox, toy);
    ctx.lineTo(tox - headlen * Math.cos(angle - Math.PI / 6), toy - headlen * Math.sin(angle - Math.PI / 6));
    ctx.moveTo(tox, toy);
    ctx.lineTo(tox - headlen * Math.cos(angle + Math.PI / 6), toy - headlen * Math.sin(angle + Math.PI / 6));
}

// ************************************************************************
// fonctions handling de l'animation
// ************************************************************************

// lancer la rotation automatique
function runMotor() {
    if (!anim_running) {
        idMotor = setInterval(animateRotor, sleep_time);
        anim_running = true;
        // stop_asked = false;
    } else {
        stop_asked = true;
    }
}

// fonction appelee par runMotor()
function animateRotor() {
    refreshGraph();
    p = p + p_inc;
    if (((p % 5) == 0) && stop_asked) {
        clearInterval(idMotor);
        anim_running = false;
        stop_asked = false;
    }
}

// faire un pas dans le sens positif
function stepRotorPlus() {
    if (!anim_running) {
        p = p + 1;
        refreshGraph();
    }
}

// faire un grand pas dans le sens positif
function stepRotorPlusPlus() {
    if (!anim_running) {
        p = p + 5;
        refreshGraph();
    }
}

// faire un pas dans le sens negatif
function stepRotorMoins() {
    if (!anim_running) {
        p = p - 1;
        if (p < 0) {
            p = 360 - 1;
        }
        refreshGraph();
    }
}

// faire un grand pas dans le sens negatif
function stepRotorMoinsMoins() {
    if (!anim_running) {
        p = p - 5;
        if (p < 0) {
            p = 360 - 5;
        }
        refreshGraph();
    }
}
function optLinesYesNo(value){
    lines_YN = !!value;
    refreshGraph();
}
function optMonophaseYesNo(value){
    monophase_YN = !!value;
	
    refreshGraph();
}
function optValeursYesNo(value){
    valeurs_YN = !!value;
	
    refreshGraph();
}


