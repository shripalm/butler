let items = document.querySelectorAll(".ms-List-cell[role='presentation']");

let transcript = Array.from(items).map(item => {
    let speaker = item.querySelector("[class^='itemDisplayName-']")?.innerText || "Unknown";
    let time = item.querySelector("[class^='baseEntry-']")?.innerText || "";


    return `${time}\n------`;
}).join("\n");

console.log(transcript);