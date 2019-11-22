function init() {

// Fonction de handling de l'affichage
// ******************************************************************
    canvas_element = document.getElementById("canvas_display_id");
    cellule_canvas = document.getElementById("cellule_canvas_id");
    cellule_input_reseaux = document.getElementById("cellule_input_reseaux_id");
    cellule_input_lignes = document.getElementById("cellule_input_lignes_id");
    cells31_input = document.getElementById("troiscells1");
    cells32_input = document.getElementById("troiscells2");
    cells33_input = document.getElementById("troiscells3");
    cells21_input = document.getElementById("deuxcells1");
    cells22_input = document.getElementById("deuxcells2");
    ctx = canvas_element.getContext("2d");

    image_de_fond = new Image();
    image_de_fond.src = '../Images/ChemEl_2.png';

    f_reduction = 0.8;
    f_reduction_w = 0.7;
    f_reduction_h = 0.8;
	scale_factor = 0.75;

    sleep_time = 100;
    id_display_values = setInterval(onResizeAction, sleep_time);

    tension_ht = 0;
    tension_mt = 0;
    tension_bt = 0;

    distance_ht = 0;
    distance_mt = 0;
    distance_bt = 0;

    pertes_ht = 0;
    pertes_mt = 0;
    pertes_bt = 0;

    pertes_ht_pc = 0;
    pertes_mt_pc = 0;
    pertes_bt_pc = 0;

    ht_color = "red";
    mt_color = "blue";
    bt_color = "green";
    txt_color = "black";

    p_home = 200000;
    p_in_bt = 300000;
    p_in_mt = 300000;
    p_in_ht = 300000;
    p_usine = 300000;

    rho_bt = 0.0175;
    rho_mt = 0.033;
    rho_ht = 0.033;

    d_bt = 6;
    d_mt = 10;
    d_ht = 15;

    onResizeAction();
}

function onResizeAction() {

//    var w_new = (f_reduction_w * window.innerWidth);
//    var h_new = (f_reduction_h * window.innerHeight);
    var w_new = (scale_factor * window.innerWidth);
    var h_new = (scale_factor * window.innerHeight);

    var letter_height = w_new / 60;
    var font_style = letter_height + "px Arial";

    cellule_input_reseaux.fontsize = letter_height;
    cellule_input_lignes.fontsize = letter_height;
    cells31_input.heifht = h_new / 3;
    cells32_input.heifht = h_new / 3;
    cells33_input.heifht = h_new / 3;
    cells21_input.heifht = h_new / 2;
    cells22_input.heifht = h_new / 2;

    cellule_canvas.width = w_new;
    cellule_canvas.height = h_new;

    canvas_element.width = w_new;
    canvas_element.height = h_new;

    ctx.drawImage(image_de_fond, 0, 0, w_new, h_new);

    const pos_ht_x = w_new * 0.4;
    const pos_ht_y = h_new * 0.2;

    const pos_mt_x = w_new * 0.75;
    const pos_mt_y = h_new * 0.45;

    const pos_bt_x = w_new * 0.45;
    const pos_bt_y = h_new * 0.8;

    const pos_maison_x = w_new * 0.1;
    const pos_maison_y = h_new * 0.8;

    const pos_usine_x = w_new * 0.1;
    const pos_usine_y = h_new * 0.4;

    var pos_box_x = w_new * 0.1;
    var pos_box_y = h_new * 0.37;
    var width_box = w_new / 4;
    var height_box = w_new / 10;

    //puissances en graphique
    const h_max_graph = w_new / 8;
    const w_max_graph = h_new / 30;
    var h_graph_p_in = 0;
    var h_graph_p_out = 0;
    var h_graph_p_pertes = 0;

    const h_graph_pos_x = w_new * 0.3;
    const h_graph_pos_y = pos_box_y;

    var mt_1_on = false;
    var mt_2_on = false;
    var mt_3_on = false;

    tension_ht = $('input[name=radio_u_ht]:checked').val();
    tension_mt = $('input[name=radio_u_mt]:checked').val();
    tension_bt = $('input[name=radio_u_bt]:checked').val();

    distance_ht = $('input[name=radio_d_ht]:checked').val();
    distance_mt = $('input[name=radio_d_mt]:checked').val();
    distance_bt = $('input[name=radio_d_bt]:checked').val();

    n_reseaux_mt = $('input[name=radio_nbre_mt]:checked').val();
    n_reseaux_bt = $('input[name=radio_nbre_bt]:checked').val();

    var p_villa = $('input[name=radio_p_villa]:checked').val();
    var n_villa = $('input[name=radio_n_villa]:checked').val();
    p_home = p_villa * n_villa;

    // Haute tension
    ctx.font = font_style;
    ctx.fillStyle = ht_color;
    ctx.fillText("HT = " + tension_ht / 1000 + " kV", pos_ht_x, pos_ht_y);
    ctx.fillText("dist =  " + distance_ht / 1000 + " km", pos_ht_x, pos_ht_y + letter_height / 4 * 5);
    if (pertes_ht > 1000) {
        ctx.fillText("pertes =  " + (pertes_ht / 1000).toFixed(0) + " kW", pos_ht_x, pos_ht_y + 2 * letter_height / 4 * 5);
    } else {
        ctx.fillText("pertes =  " + (pertes_ht).toFixed(0) + " W", pos_ht_x, pos_ht_y + 2 * letter_height / 4 * 5);
    }

    // Moyenne tension
    ctx.fillStyle = mt_color;
    ctx.fillText("MT = " + tension_mt / 1000 + " kV", pos_mt_x, pos_mt_y);
    ctx.fillText("dist =  " + distance_mt / 1000 + " km", pos_mt_x, pos_mt_y + letter_height / 4 * 5);
    if (pertes_mt > 1000) {
        ctx.fillText("pertes =  " + (pertes_mt / 1000).toFixed(0) + " kW", pos_mt_x, pos_mt_y + 2 * letter_height / 4 * 5);
    } else {
        ctx.fillText("pertes =  " + (pertes_mt).toFixed(0) + " W", pos_mt_x, pos_mt_y + 2 * letter_height / 4 * 5);
    }

    // Basse tension
    ctx.fillStyle = bt_color;
    ctx.fillText("BT = " + tension_bt + " V", pos_bt_x, pos_bt_y);
    ctx.fillText("dist = " + distance_bt + " m", pos_bt_x, pos_bt_y + letter_height / 4 * 5);
    if (pertes_bt > 1000) {
        ctx.fillText("pertes =  " + (pertes_bt / 1000).toFixed(0) + " kW", pos_bt_x, pos_bt_y + 2 * letter_height / 4 * 5);
    } else {
        ctx.fillText("pertes =  " + (pertes_bt).toFixed(0) + " W", pos_bt_x, pos_bt_y + 2 * letter_height / 4 * 5);
    }

    // Village
    ctx.fillStyle = txt_color;
    ctx.fillText(n_reseaux_bt + " groupes de " + n_villa + " villas à " + p_villa / 1000 + " kW / villa", pos_maison_x, pos_maison_y);
    // ctx.fillText("Puissance utile totale = " + n_reseaux_bt + " fois " + p_home/1000 + " kW",pos_maison_x, pos_maison_y + letter_height/4*5);

    ctx.fillText("Puissance fournie", pos_usine_x, pos_usine_y);
    ctx.fillText((p_in_ht / 1000).toFixed(0) + " kW", pos_usine_x, pos_usine_y + letter_height / 4 * 5);

    // résultat global
    ctx.beginPath();
    ctx.lineWidth = "1";
    ctx.fillStyle = "LightGoldenRodYellow";
    ctx.strokeStyle = "black";
    pos_box_x = h_graph_pos_x + 2 * w_max_graph + +1.3 * w_max_graph;
    ctx.rect(pos_box_x, pos_box_y, width_box, h_max_graph, 100);
    ctx.stroke();
    ctx.fill();

    var p_pertes_totales = pertes_ht + pertes_mt * n_reseaux_mt + pertes_bt * n_reseaux_bt * n_reseaux_mt;
    var p_utile_totale = p_home * n_reseaux_bt * n_reseaux_mt;
    calculate_lost();
    ctx.fillStyle = "blue";
    ctx.fillText("Puissance fournie = " + (p_in_ht / 1000).toFixed(0) + " kW", pos_box_x + 5, pos_box_y + 1.5 * letter_height / 4 * 5);
    ctx.fillStyle = "red";
    ctx.fillText("Pertes totales = " + (p_pertes_totales / 1000).toFixed(0) + " kW", pos_box_x + 5, pos_box_y + 2.5 * letter_height / 4 * 5);
    ctx.fillStyle = "green";
    ctx.fillText("Puissance utile = " + (p_utile_totale / 1000).toFixed(0) + " kW", pos_box_x + 5, pos_box_y + 3.5 * letter_height / 4 * 5);
    ctx.fillStyle = "black";
    ctx.fillText("Rendement = " + (p_utile_totale / p_in_ht * 100).toFixed(2) + " %", pos_box_x + 5, pos_box_y + 4.5 * letter_height / 4 * 5);

    h_graph_p_in = h_max_graph;
    h_graph_p_out = h_max_graph * p_utile_totale / p_in_ht;
    h_graph_p_pertes = h_max_graph * p_pertes_totales / p_in_ht;

    // P usine
    ctx.beginPath();
    ctx.lineWidth = "1";
    ctx.strokeStyle = "black";
    ctx.fillStyle = "lightblue";
    ctx.rect(h_graph_pos_x, h_graph_pos_y, w_max_graph, h_graph_p_in, 100);
    ctx.stroke();
    ctx.fill();

    // P pertes
    ctx.beginPath();
    ctx.fillStyle = "lightpink";
    ctx.rect(h_graph_pos_x + 1.3 * w_max_graph, h_graph_pos_y, w_max_graph, h_graph_p_pertes, 100);
    ctx.stroke();
    ctx.fill();

    // P utile
    ctx.beginPath();
    ctx.fillStyle = "lightgreen";
    ctx.rect(h_graph_pos_x + 1.3 * w_max_graph, h_graph_pos_y + h_graph_p_pertes, w_max_graph, h_graph_p_out, 100);
    ctx.stroke();
    ctx.fill();
}

function calculate_lost() {

    const u_bt = tension_bt;
    const u_mt = tension_mt;
    const u_ht = tension_ht;

    const dist_bt = distance_bt;
    const dist_mt = distance_mt;
    const dist_ht = distance_ht;

    // basse tension
    const i_bt = p_home / u_bt;
    const s_bt = Math.PI * Math.pow(d_bt, 2) / 4;
    const r_bt = 2 * rho_bt * dist_bt / s_bt;
    pertes_bt = r_bt * Math.pow(i_bt, 2);
    p_in_bt = (p_home + pertes_bt) * n_reseaux_bt;
    pertes_bt_pc = pertes_bt / (p_home + pertes_bt);

    // moyenne tension
    const i_mt = p_in_bt / u_mt;
    const s_mt = Math.PI * Math.pow(d_mt, 2) / 4;
    const r_mt = 2 * rho_mt * dist_mt / s_mt;
    pertes_mt = r_mt * Math.pow(i_mt, 2);
    p_in_mt = (p_in_bt + pertes_mt) * n_reseaux_mt;
    pertes_mt_pc = pertes_mt / (p_in_bt + pertes_mt);

    // haute tension
    const i_ht = p_in_mt / u_ht;
    const s_ht = Math.PI * Math.pow(d_ht, 2) / 4;
    const r_ht = 2 * rho_ht * dist_ht / s_ht;
    pertes_ht = r_ht * Math.pow(i_ht, 2);
    p_in_ht = p_in_mt + pertes_ht;
    pertes_ht_pc = pertes_ht / p_in_ht;
}

