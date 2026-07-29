/* ========================= */
/* FUENTES Y CONFIGURACIÓN   */
/* ========================= */

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{

    font-family:'Cormorant Garamond', serif;

    color:#f5e9c8;

    background:
    radial-gradient(circle at top,#5b0000 0%,#2a0000 45%,#120000 100%);

    overflow-x:hidden;

}

/* ========================= */
/* CORTINAS                  */
/* ========================= */

.curtain{

    position:fixed;

    top:0;

    width:180px;

    height:100vh;

    z-index:-1;

    background:
    repeating-linear-gradient(
        90deg,
        #420000 0px,
        #6d0000 18px,
        #8a0000 34px,
        #5b0000 52px
    );

    box-shadow:
    inset -20px 0 30px rgba(0,0,0,.5),
    inset 20px 0 30px rgba(255,255,255,.08);

}

.left{

    left:0;

}

.right{

    right:0;

}

/* ========================= */
/* CABECERA                  */
/* ========================= */

header{

    display:flex;

    justify-content:center;

    margin-top:40px;

}

/* ========================= */
/* MARQUESINA                */
/* ========================= */

.marquee{

    width:900px;

    max-width:90%;

    text-align:center;

    padding:35px;

    background:#efe1b4;

    border-radius:20px;

    border:12px solid #8d5b00;

    box-shadow:

    0 0 50px rgba(255,215,0,.45),

    inset 0 0 30px white;

    position:relative;

}

/* Bombillas */

.marquee::before{

content:"";

position:absolute;

left:-14px;

right:-14px;

top:-14px;

bottom:-14px;

border-radius:26px;

background:

radial-gradient(circle,#ffd65c 2px,transparent 3px);

background-size:24px 24px;

z-index:-1;

filter:drop-shadow(0 0 8px gold);

}

.marquee h1{

font-family:'Cinzel',serif;

font-size:72px;

color:#4b1200;

letter-spacing:5px;

}

.marquee p{

margin-top:10px;

font-size:34px;

letter-spacing:4px;

color:#7c3400;

}

/* ========================= */
/* ESCENARIO                 */
/* ========================= */

main{

width:1200px;

max-width:92%;

margin:70px auto;

padding:50px;

background:

linear-gradient(
180deg,
rgba(40,0,0,.2),
rgba(0,0,0,.35));

border:4px solid rgba(255,215,0,.25);

border-radius:20px;

box-shadow:

0 0 50px rgba(0,0,0,.7);

}

/* Piso */

main::after{

content:"";

display:block;

margin-top:60px;

height:130px;

background:

repeating-linear-gradient(
90deg,
#4b2b12,
#693d1b 20px,
#4d2a14 40px);

border-radius:12px;

box-shadow:inset 0 10px 20px rgba(255,255,255,.15);

}

/* ========================= */
/* TITULOS DE CATEGORIA      */
/* ========================= */

h2{

font-family:'Cinzel';

font-size:48px;

text-align:center;

margin:60px 0 30px;

color:#f4d26d;

text-shadow:

0 0 12px gold;

}

footer{

text-align:center;

padding:40px;

font-size:28px;

color:#f6df94;

}