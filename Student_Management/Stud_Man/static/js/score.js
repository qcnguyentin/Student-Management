function spinner(status="block") {
    let s = document.getElementsByClassName("my-spinner")
    for (let i = 0; i < s.length; i++)
        s[i].style.display = status
}

function loadScores() {
    spinner()
    fetch(`/api/score/score-list`).then(res => res.json()).then(data => {
        spinner("none")
        let h = "";
        data.forEach(s => {
            h += `
                <tr class="tb-notification-content" id="score${s.score_id}">
                    <td class="${ s.student_name}"> ${ s.student_name}</td>
                    <td>${ s.type_score }</td>
                    <td>${ s.score }</td>
                    <td>${ s.class_name }</td>
                    <td>${ s.subject_name }</td>
                    <td>Học kỳ ${ s.semester }, Năm ${ s.year }</td>
                    <td>
                        <input type="button" value="Sửa">
                        <input type="button" value="Xóa">
                    </td>
                </tr>
            `
        })
        console.info(h)
        let d = document.getElementById("tb-scores")
        d.innerHTML += h;
    })
}
//
//function addToScore(student_name, type_score, score) {
//    fetch("/api/score", {
//        method: "post",
//        body: JSON.stringify({
//            "student_name": student_name,
//            "type_score": type_score,
//            "score": score
//        }),
//        headers: {
//            "Content-Type": "application/json"
//        }
//    })
//}

function checkValue() {
    let a = document.getElementsByClassName("1")
    for (let i = 0; i < a.length; i++)
        console.info(a[i].value)
}