const data = {};
data["verify.yml"] = (function () {
    const req = new XMLHttpRequest();
    req.open("GET", "https://raw.githubusercontent.com/kmyk/online-judge-verify-helper/master/.github/workflows/verify.yml", false);
    req.send();
    return req.responseText;
})();
data["example.test.cpp"] = (function () {
    const req = new XMLHttpRequest();
    req.open("GET", "https://raw.githubusercontent.com/kmyk/online-judge-verify-helper/master/example.test.cpp", false);
    req.send();
    return req.responseText;
})();

const input = document.getElementById("input");
const output = document.getElementById("output");
const output2 = document.getElementById("output2");
const output3 = document.getElementById("output3");
const output4 = document.getElementById("output4");
const output5 = document.getElementById("output5");
const output6 = document.getElementById("output6");
const output7 = document.getElementById("output7");
function update() {
    if (input.value.match(/\/github.com\/[^\/]+\/[^\/]+/)) {
        const url = input.value.replace(/\/$/, "");

        const filename = ".github%2Fworkflows%2Fverify.yml"
        const value = encodeURIComponent(data["verify.yml"].replace("git+https://github.com/kmyk/online-judge-verify-helper.git@master", "online-judge-verify-helper"));
        output.href = url + "/new/master?filename=" + filename + "&value=" + value;
        output.textContent = url + "&value=...";

        const filename2 = "example.test.cpp";
        const value2 = encodeURIComponent(data["example.test.cpp"]);
        output2.href = url + "/new/master?filename=" + filename2 + "&value=" + value2;

        output3.href = input.value.replace(/\/$/, "") + "/actions";
        output5.href = input.value.replace(/\/$/, "") + "/actions";

        output4.textContent = "[![Actions Status](" + url + "/workflows/verify/badge.svg)](" + url + "/actions)";
        output6.src = url + "/workflows/verify/badge.svg";
        output7.src = url + "/workflows/verify/badge.svg";
    }
}
input.addEventListener('change', update);
input.addEventListener('keyup', update);
update();
