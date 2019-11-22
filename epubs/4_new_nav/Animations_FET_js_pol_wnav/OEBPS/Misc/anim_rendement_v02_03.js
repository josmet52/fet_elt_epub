function initRendement() {

    canvas_element = document.getElementById("canvas_display_id");
    ctx = canvas_element.getContext("2d");

    image_de_fond = new Image();
    image_de_fond.src = '../Images/rendement_1f.png';

    // f_reduction_w = 0.85;
    // f_reduction_h = 0.85;

    r_turbine = document.getElementById("slider_turbine_id");
    r_alternateur = document.getElementById("slider_alternateur_id");
    r_transfo = document.getElementById("slider_transfo_id");

    txt_turbine = document.getElementById("r_turbine_id");
    txt_alternateur = document.getElementById("r_alternateur_id");
    txt_transfo = document.getElementById("r_transfo_id");

    p_in = 1000;
    n1 = r_turbine.value / 100; //0.8;
    n2 = r_alternateur.value / 100; //0.9;
    n3 = r_transfo.value / 100; //0.95;

    sleep_time = 100;
    id_display_values = setInterval(displayValueRendement, sleep_time);

    onResizeActionRendement();
}

function displayValueRendement() {
    n1 = r_turbine.value / 100;
    n2 = r_alternateur.value / 100;
    n3 = r_transfo.value / 100;

    txt_turbine.innerHTML = "η = " + r_turbine.value + "%";
    txt_alternateur.innerHTML = "η = " + r_alternateur.value + "%";
    txt_transfo.innerHTML = "η = " + r_transfo.value + "%";

    onResizeActionRendement();
}

function onResizeActionRendement() {

    // var disp_w = (f_reduction_w * window.innerWidth);
    // var disp_h = (f_reduction_h * window.innerHeight);
    var scale_factor = 0.85;
    var disp_w = (scale_factor * window.innerWidth);
    var disp_h = (scale_factor * window.innerHeight);

    canvas_element.width = disp_w;
    canvas_element.height = disp_h;

    var letter_height = String(disp_w / 60);
    var font_style = letter_height + "px Georgia";
    ctx.font = font_style;

    var r_h = disp_h * 0.25;
    var r_w = disp_w * 0.9;

    lf = r_w / 100;
    lf_inout = r_w / 40;

    ctx.drawImage(image_de_fond, 0, 0, disp_w, disp_h);

    var x0 = 0;
    var x1 = 0;
    var x2 = 0;
    var x3 = 0;
    var x4 = 0;
    var x5 = 0;
    var x6 = 0;
    var x7 = 0;
    var y0 = 0;
    var y1 = 0;
    var y2 = 0;
    var y3 = 0;
    var y4 = 0;
    var y5 = 0;

    x0 = (disp_w - r_w) / 2;
    y0 = disp_h * 0.65;
    y1 = y0 + r_h * 0.9;

    var r_in = y1 -y0;
    var r_2 = r_in * n1;
    var r_3 = r_2 * n2;
    var r_4 = r_3 * n3;

    y2 = y0 + r_2;
    y3 = y0 + r_3;
    y4 = y0 + r_4;
    y5 = y0 + r_h * 0.95;

    x1 = 0.25 * disp_w;
    x2 = x1 + r_in * (1 - n1);
    x3 = 0.47 * disp_w ;
    r_2 = r_in * n1;
    x4 = x3 + r_2 * ( 1 - n2);
    x5 = 0.77 * disp_w ;
    r_3 = r_2 * n2;
    x6 = x5 + r_3 * (1 - n3);
    x7 = 0.93 * disp_w ;

    const color_p_utile = "#f1f1f1"; //"#b2fff4";
    const color_hydro = "#66c9ff";
    const color_alternateur = "#ffda07"; //"#b0ceec"; //"#32cd32"; // LimeGreen
    const color_transfo = "#8dd900";
    const color_border = "#777777";
    const color_text = "#000000";
    const color_white = "#FFFFFF";
    const color_yellow = "#FFFF00";

    ctx.strokeStyle = color_border; // color_p_utile;
    ctx.fillStyle = color_p_utile;

    // pertes turbine
    ctx.beginPath();
    // ctx.moveTo(x0, y2);
    // ctx.lineTo(x0, y1);
    // ctx.lineTo(x1, y1);
    // ctx.lineTo(x1, y5);
    // ctx.lineTo(x2, y5);
    // ctx.lineTo(x2, y2);
    ctx.moveTo(x1, y2);
    ctx.lineTo(x1, y5);
    ctx.lineTo(x1 - lf, y5);
    ctx.lineTo(x1 + ( x2- x1) / 2, y5 + lf);
    ctx.lineTo(x2 + lf, y5);
    ctx.lineTo(x2, y5);
    ctx.lineTo(x2, y2);
    ctx.closePath();
    ctx.fillStyle = color_hydro;
    // ctx.strokeStyle = color_hydro;
    ctx.stroke();
    ctx.fill();
    // ctx.fillRect(x1, y1, x2, y5);
    // ctx.fill();

    // pertes alternateur
    ctx.beginPath();
    // ctx.moveTo(x2, y2);
    // ctx.lineTo(x3, y2);
    // ctx.lineTo(x3, y5);
    // ctx.lineTo(x4, y5);
    // ctx.lineTo(x4, y3);
    // ctx.lineTo(x2, y3);
    ctx.moveTo(x3, y3);
    ctx.lineTo(x3, y5);
    ctx.lineTo(x3 - lf, y5);
    ctx.lineTo(x3 + ( x4- x3) / 2, y5 + lf);
    ctx.lineTo(x4 + lf, y5);
    ctx.lineTo(x4, y5);
    ctx.lineTo(x4, y3);
    ctx.closePath();
    // ctx.strokeStyle = color_alternateur;
    ctx.fillStyle = color_alternateur;
    ctx.stroke();
    ctx.fill();

    // pertes transformateur
    ctx.beginPath();
    // ctx.moveTo(x4, y3);
    // ctx.lineTo(x5, y3);
    // ctx.lineTo(x5, y5);
    // ctx.lineTo(x6, y5);
    // ctx.lineTo(x6, y4);
    // ctx.lineTo(x4, y4);
    ctx.moveTo(x5, y4);
    ctx.lineTo(x5, y5);
    ctx.lineTo(x5 - lf, y5);
    ctx.lineTo(x5 + ( x6- x5) / 2, y5 + lf);
    ctx.lineTo(x6 + lf, y5);
    ctx.lineTo(x6, y5);
    ctx.lineTo(x6, y4);
    ctx.closePath();
    // ctx.strokeStyle = color_transfo;
    ctx.fillStyle = color_transfo;
    ctx.stroke();
    ctx.fill();

    // puissance utile
    ctx.beginPath();
    ctx.moveTo(x0, y1);
    ctx.lineTo(x1, y1);
    ctx.lineTo(x1, y2);
    ctx.lineTo(x3, y2);
    ctx.lineTo(x3, y3);
    ctx.lineTo(x5, y3);
    ctx.lineTo(x5, y4);

    // ctx.lineTo(x2, y2);
    // ctx.lineTo(x2, y3);
    // ctx.lineTo(x4, y3);
    // ctx.lineTo(x4, y4);
    // ctx.lineTo(x6, y4);

    ctx.lineTo(x7, y4);
    ctx.lineTo(x7, y4 + lf);
    ctx.lineTo(x7 + lf_inout, y0 + (y4 - y0) / 2);
    ctx.lineTo(x7, y0 - lf);
    ctx.lineTo(x7, y0);
    ctx.lineTo(x0,y0);
    ctx.lineTo(x0 + lf_inout, y0 + (y1 - y0) / 2);
    ctx.closePath();
    ctx.fillStyle = color_p_utile;
    ctx.fill();
    ctx.stroke();

    // Puissance utile
    ctx.moveTo(x0,y0); // --> A
    ctx.lineTo(x0 + lf_inout, y0 + (y1 - y0) / 2);
    ctx.lineTo(x0, y1); // --> C
    ctx.lineTo(x1, y1); // --> D

    ctx.lineTo(x1, y5);
    ctx.lineTo(x1 - lf, y5);
    ctx.lineTo(x1 + (x2 - x1) / 2, y5 + lf);
    ctx.lineTo(x2 + lf, y5);
    ctx.lineTo(x2, y5);
    ctx.lineTo(x2, y2); // --> E

    ctx.lineTo(x3, y2); // --> F

    ctx.lineTo(x3, y5);
    ctx.lineTo(x3 - lf, y5);
    ctx.lineTo(x3 + (x4 - x3) / 2, y5 + lf);
    ctx.lineTo(x4 + lf, y5);
    ctx.lineTo(x4, y5);
    ctx.lineTo(x4, y3); // --> g

    ctx.lineTo(x5, y3); // --> H

    ctx.lineTo(x5, y5);
    ctx.lineTo(x5 - lf, y5);
    ctx.lineTo(x5 + (x6 - x5) / 2, y5 + lf);
    ctx.lineTo(x6 + lf, y5);
    ctx.lineTo(x6, y5);
    ctx.lineTo(x6, y4); // --> I
    ctx.lineTo(x7, y4); // --> J

    ctx.lineTo(x7, y4 + lf);
    ctx.lineTo(x7 + lf_inout, y0 + (y4 - y0) / 2);
    ctx.lineTo(x7, y0 - lf);
    ctx.lineTo(x7, y0); // --> K

    ctx.lineTo(x0, y0); // --> A
    ctx.stroke();

    ctx.fillStyle = color_text;
    var p_in = 1000;
    var p_arbre = p_in * n1;
    var p_el = p_arbre * n2;
    var p_out = p_el * n3;
    var n_global = n1 * n2 * n3;

    ctx.fillText("P absorbée = " + (p_in ).toFixed(0) + " W", x0 + 1.5 * lf_inout, y0 + (y1 - y0) / 2 + letter_height / 2);
    ctx.fillText("P arbre = " + (p_arbre).toFixed(0) + " W", x2 , y0 + (y2 - y0) / 2.5 + letter_height / 2);
    ctx.fillText("P electrique = " + (p_el ).toFixed(0) + " W", x4, y0 + (y3 - y0) / 2 + letter_height / 2);
    ctx.fillText("P utile = " + (p_out).toFixed(0) + " W", x6, y0 + (y4 - y0) / 2 + letter_height / 2);

    var pertes_turbine = p_in * (1-n1);
    var pertes_alternateur = p_arbre * (1 - n2);
    var pertes_transfo = p_el * ( 1 - n3);

    var y6 = y5 + 4 * lf;
    var y7 = r_h * 1;

    ctx.fillStyle = color_text;
    ctx.fillText("Pertes :", x0 , y6);

    ctx.fillStyle = color_text;
    ctx.fillText("turbine = " + pertes_turbine.toFixed(0) + " W", x0 + (x1 - x0) / 2, y6);
    ctx.fillStyle = color_white;
    ctx.fillText("η = " + n1.toFixed(2), 0.92 * x1, r_h * 0.7);

    ctx.fillStyle = color_text;
    ctx.fillText("alternateur = " + pertes_alternateur.toFixed(0) + " W", x2 + (x3 - x2) / 2, y6);
    ctx.fillStyle = color_white;
    ctx.fillText("η = " + n2.toFixed(2), 0.97 * x3, y7);

    ctx.fillStyle = color_text;
    ctx.fillText("transfo = " + pertes_transfo.toFixed(0) + " W", x4 + (x5 - x4) / 1.5, y6);
    ctx.fillStyle = color_white;
    ctx.fillText("η = " + n3.toFixed(2), 0.97 * x5, y7);

    ctx.fillStyle = color_text;
    ctx.fillText("Rendement global = " + n_global.toFixed(3), disp_w * 0.4, y0 - 2 * lf);


}

