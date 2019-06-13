// ==UserScript==
// @name         Crunchyroll Skip Intro
// @namespace    HKG
// @version      0.1
// @description  should be self-explanatory.
// @author       HKG
// @match        https://www.crunchyroll.com/*/*
// @downloadURL  https://github.com/HKGx/Crunchyroll-Skip-Intro/raw/master/Tampermonkey/main.user.js
// @updateURL    https://github.com/HKGx/Crunchyroll-Skip-Intro/raw/master/Tampermonkey/meta.user.js
// ==/UserScript==

var player;
var url = "51.68.142.188:5000/";
var menu;
var timeChange = undefined;

const customCSS =
    ".tofade {\n    opacity: 1;\n    transition: opacity 500ms;\n}\n.tofade.fade {\n    opacity: 0;\n}";

function onSkipClicked() {
    if (timeChange < 0) {
        return createMessage("Couldn't load info about intro end.", "#ff6961");
    }
    if (timeChange == 0){
        return createMessage("Episode has no intro.", "#77dd77")
    }
    VILOS_PLAYERJS.setCurrentTime(timeChange);
}
function getTimeChange() {
    try {
        const pathname = new URL(window.location.href).pathname;
        const episodeName = pathname.split("/")[2].split("-");
        const episode = episodeName[episodeName.length - 1];
        fetch(`${url}skipper/${episode}`).then(x =>
            x.text().then(x => {
                const time = parseFloat(x);
                if(time < 0) {return;}
                timeChange = time;
            })
        );
    } catch (error) {
        return false;
    }
    return true;
}

const addNeccesaryClasses = obj => obj.classList.add("facebook", "left");
const fadeAndRemove = (obj, time = 2500) =>
    setTimeout(() => {
        obj.classList.add("fade");
        setTimeout(() => obj.remove(), 500);
    }, time);

function createMessage(text, color) {
    if (document.getElementById("skipperMessage")) {
        return;
    }
    let span = document.createElement("span");
    span.id = "skipperMessage";
    addNeccesaryClasses(span);
    span.classList.add("tofade");
    let p = document.createElement("p");
    p.style.color = color;
    p.textContent = text;
    span.appendChild(p);
    menu.appendChild(span);
    fadeAndRemove(span);
}
function createSkipButton() {
    const twitter = document.getElementsByClassName("twitter")[0];
    twitter.style.marginRight = "12px";
    let span = document.createElement("span");
    span.classList.add("facebook");
    span.classList.add("left");
    let buttonChild = document.createElement("button");
    buttonChild.textContent = "SKIP";
    buttonChild.style.width = "60px";
    buttonChild.style.height = "20px";
    buttonChild.addEventListener("click", onSkipClicked);
    span.appendChild(buttonChild);
    menu.appendChild(span);
}
function onLoad() {
    const newStyle = document.createElement("style");
    newStyle.innerHTML = customCSS;
    document.body.append(newStyle);
    menu = document.getElementsByClassName(
        "showmedia-submenu white-wrapper cf container-shadow small-margin-bottom"
    )[0];
    if (!getTimeChange()) return;
    if (!createSkipButton()) return;
}

(function () {
    window.addEventListener("load", onLoad);
})();
