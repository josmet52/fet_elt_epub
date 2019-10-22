// Fonction de handling de l'affichage
// ******************************************************************

function onResizeActionOscillo() {
	

    if (show_oscillo) {
        cel_cde_osc.style.display = "table-cell";
    } else {
        cel_cde_osc.style.display = "none";
        cel_canvas.style.borderRight = "1px solid black";
        cel_canvas.style.borderRadius= "10px 10px 10px 10px";
  }

    if (show_tension) {
        cel_tension.style.display = "table-cell";
    } else {
        cel_tension.style.display = "none";
    }

    if (show_frequence) {
        cel_frequence.style.display = "table-cell";
    } else {
        cel_frequence.style.display = "none";
    }

    if (show_phase) {
        cel_phase.style.display = "table-cell";
    } else {
        cel_phase.style.display = "none";
    }

    var w = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    var h = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

    xy_factor = 1.2;
    h_factor = 0.75;
    if (h <= w) {
        h0 = h * h_factor;
        w0 = h0 * xy_factor ;
    } 
    else {
        h0 = w * h_factor;
        w0 = h0 * xy_factor;
    }

    cel_tension.width = h0 / 3 ;
    cel_phase.width = h0 / 3 ;
    cel_frequence.width = h0 / 3 ;

    const f_reduction = 2;
    tab_main.width = f_reduction * w0 + "px";

    canvas_element.height = h0;
    canvas_element.width = w0;

    cel_cde_osc_vdiv.style.paddingTop = "5px" ;
    cel_cde_osc_msdiv.style.paddingTop = "10px" ;

    xy_margin = 5;
    line_width = 1;

    ctx.clearRect(0, 0, w0, h0);
    ctx.stroke();

    // dimension des éléments
    r_display_x = (w0 - 2 * xy_margin - 2 * line_width);
    x_0 = (w0 / 2);
    x_min = (-r_display_x / 2);
    x_max = (r_display_x / 2);

    r_display_y = (h0 - 2 * xy_margin - 2 * line_width);
    y_0 = (h0 / 2);
    y_min = (-r_display_y / 2);
    y_max = (r_display_y / 2);

    displayValueOscillo();
}

function displayValueOscillo() {

    amp_crete = parseInt(slide_ampl.value);
    amp_eff = parseInt(amp_crete / Math.sqrt(2));
    amp_pp = parseInt(amp_crete * 2);
    freq = parseInt(slide_freq.value);
    periode = (1000 / freq).toPrecision(3);
    phase = parseInt(slide_phase.value);
    lbl_amplval.innerHTML = "U<sub>efficace</sub> = " + amp_eff + "V<br/>U<sub>crête</sub> = " + amp_crete + "V<br/>U<sub>pp</sub> = " + amp_pp + "V";
    lbl_ampl.innerHTML = "Amplitude<br/>[" + String(volt_div) + " V/div]";
    lbl_freqval.innerHTML = "Fréquence = " + freq + " Hz<br/>Période = " + periode + " ms";
    lbl_freq.innerHTML = "Fréquence<br/>[" + String(ms_div) + " ms/div]";

    lbl_phaseval.innerHTML = "Phase = " + phase + " \u00b0<br/>Phase = " + (phase / 360 * 2 * Math.PI).toFixed(2) + " rad";
    angle_div = parseInt(360 / periode * ms_div);
    lbl_phase.innerHTML = "Phase<br/>[" + String(angle_div) + " \u00b0/div]";

    drawOscilloGrid(ctx, r_display_x, r_display_y, xy_margin);
    drawSinusOscillo();
}

// Fonction de l'animation
// ******************************************************************

// afficher la grille
function drawOscilloGrid(ctx, r_display_width, r_display_height, xy_zero) {

    // dessiner la face avant de l'oscillosope
    // le cadre
    ctx.strokeStyle = color_border_ecran;
    ctx.fillStyle = color_fond_ecran;
    ctx.lineWidth = line_width;

    ctx.beginPath();
    ctx.rect(xy_zero, xy_zero, r_display_width, r_display_height);
    ctx.stroke();
    ctx.fillRect(xy_zero, xy_zero, r_display_width, r_display_height);
    ctx.fill();

    // la grille
    ctx.translate(x_0, y_0);
    ctx.strokeStyle = color_divison_ecran;
    // divisions verticales
    ctx.setLineDash([3, 3]);
    ctx.beginPath();
    x_step = (r_display_width) / nbre_grid;
    i_min = -parseInt(nbre_grid / 2);
    i_max = nbre_grid - i_min;
    for (i = i_min; i < i_max; i++) {
        ctx.moveTo(i * x_step, y_min);
        ctx.lineTo(i * x_step, y_max);
    }
    ctx.stroke();

    ctx.beginPath();
    ctx.setLineDash([]);
    ctx.moveTo(0, y_min);
    ctx.lineTo(0, y_max);
    ctx.stroke();

    // divisions horizontales
    ctx.setLineDash([3, 3]);
    ctx.beginPath();
    y_step = (r_display_y) / 8;
    for (i = -3; i < 4; i++) {
        ctx.moveTo(x_min, i * y_step);
        ctx.lineTo(x_max, i * y_step);
    }
    ctx.stroke();

    ctx.beginPath();
    ctx.setLineDash([]);
    ctx.moveTo(x_min, 0);
    ctx.lineTo(x_max, 0);
    ctx.stroke();

    ctx.translate(-x_0, -y_0);
}

// afficher le sinus
function drawSinusOscillo() {

    ctx.translate(x_0, y_0);

    var T;
    var t_max;
    var phi_max;
    var nbre_pts = freq;
    var i = 0;
    T = 1000 / freq;
    t_max = nbre_grid * ms_div;
    phi_max = 2 * Math.PI * t_max / T;
    amp_max = volt_div * 8;

    //sinus de reference sans dephasage
    ctx.strokeStyle = sinus_ref_color;
    ctx.lineWidth = line_width * 2;
    nbre_pts = 10000;

    phase_rad = 0; //phase/180*Math.PI;
    x_old = x_min;
    y_old = -Math.sin(phase_rad) * y_max * amp_crete / amp_max * 2;
    ctx.moveTo(x_old, y_old);
    ctx.beginPath();

    for (i = 0; i < nbre_pts; i++) {

        t = i / nbre_pts * t_max;
        phi_rad = t / t_max * phi_max; //+phase_rad;
        y_new = -Math.sin(phi_rad) * y_max * amp_crete / amp_max * 2;

        x_pos = i / nbre_pts;
        x_new = (x_min + x_pos * (x_max - x_min));

        if ((Math.abs(y_new) <= (y_max)) && (Math.abs(y_old) <= (y_max))) {
            ctx.moveTo(x_old, y_old);
            ctx.lineTo(x_new, y_new);
        }

        x_old = x_new;
        y_old = y_new;
    }
    ctx.stroke();
    ctx.lineWidth = line_width;

    // sinus avaec dephasage
    ctx.strokeStyle = color_courbe_1;
    ctx.lineWidth = line_width * 2;
    nbre_pts = 10000;

    phase_rad = phase / 180 * Math.PI;
    x_old = x_min;
    y_old = -Math.sin(phase_rad) * y_max * amp_crete / amp_max * 2;
    ctx.moveTo(x_old, y_old);
    ctx.beginPath();

    for (i = 0; i < nbre_pts; i++) {

        t = i / nbre_pts * t_max;
        phi_rad = t / t_max * phi_max + phase_rad;
        y_new = -Math.sin(phi_rad) * y_max * amp_crete / amp_max * 2;

        x_pos = i / nbre_pts;
        x_new = (x_min + x_pos * (x_max - x_min));

        if ((Math.abs(y_new) <= (y_max)) && (Math.abs(y_old) <= (y_max))) {
            ctx.moveTo(x_old, y_old);
            ctx.lineTo(x_new, y_new);
        }

        x_old = x_new;
        y_old = y_new;
    }
    ctx.stroke();
    ctx.lineWidth = line_width;


    ctx.translate(-x_0, -y_0);
}


// Fonction commandes
// ******************************************************************
function btnVoltPlus() {
    if (volt_div == 100) {
        volt_div = 200;
    }
    if (volt_div == 50) {
        volt_div = 100;
    }
    if (volt_div == 20) {
        volt_div = 50;
    }
    if (volt_div == 10) {
        volt_div = 20;
    }
    if (volt_div == 5) {
        volt_div = 10;
    }
    if (volt_div == 2) {
        volt_div = 5;
    }
    if (volt_div == 1) {
        volt_div = 2;
    }
    lbl_volt.innerHTML = volt_div + " V/div";
}

function btnVoltMoins() {
    if (volt_div == 2) {
        volt_div = 1;
    }
    if (volt_div == 5) {
        volt_div = 2;
    }
    if (volt_div == 10) {
        volt_div = 5;
    }
    if (volt_div == 20) {
        volt_div = 10;
    }
    if (volt_div == 50) {
        volt_div = 20;
    }
    if (volt_div == 100) {
        volt_div = 50;
    }
    if (volt_div == 200) {
        volt_div = 100;
    }
    lbl_volt.innerHTML = volt_div + " V/div";
}

function btnDivPlus() {
    if (ms_div == 5) {
        ms_div = 10;
    }
    if (ms_div == 2) {
        ms_div = 5;
    }
    if (ms_div == 1) {
        ms_div = 2;
    }
    if (ms_div == 0.5) {
        ms_div = 1;
    }
    if (ms_div == 0.2) {
        ms_div = 0.5;
    }
    if (ms_div == 0.1) {
        ms_div = 0.2;
    }
    lbl_div.innerHTML = ms_div + " ms/div";
}

function btnDivMoins() {
    if (ms_div == 0.2) {
        ms_div = 0.1;
    }
    if (ms_div == 0.5) {
        ms_div = 0.2;
    }
    if (ms_div == 1) {
        ms_div = 0.5;
    }
    if (ms_div == 2) {
        ms_div = 1;
    }
    if (ms_div == 5) {
        ms_div = 2;
    }
    if (ms_div == 10) {
        ms_div = 5;
    }
    lbl_div.innerHTML = ms_div + " ms/div";
}

// Fonction utilitaires
// ******************************************************************

function showHideElementOscillo() {

    show_phase = !show_phase;
    show_oscillo = !show_oscillo;
    show_logo = !show_logo;
    onResizeActionOscillo();
}
