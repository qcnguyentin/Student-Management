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
                        <button type="button" class="btn btn-secondary" data-bs-toggle="modal" data-bs-target="#myModal-update">
                            Sửa
                        </button>
                        <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#myModal-delete">
                            Xóa
                        </button>
                    </td>
                </tr>
            `
        })
        let d = document.getElementById("tb-scores")
        d.innerHTML += h;
    })
}


function addScore() {
    spinner()
    fetch(`/api/score/score-list`, {
        method: "post",
        body: JSON.stringify({
            'student_name': document.getElementById("add-score-student").value,
            'score': document.getElementById("add-score-score").value,
            'type_score': document.getElementById("add-score-type").value,
            'class_name': document.getElementById("add-score-class").value,
            'semester': document.getElementById("add-score-semester").value,
            'subject_name': document.getElementById("add-score-subject").value,
            'year': document.getElementById("add-score-year").value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => res.json()).then((data) => {
        spinner("none")
       if (data.status == 204) {
            let s = data.score
            alert("Thêm thành công")
            let h = `
                <tr class="tb-notification-content" id="score${s.score_id}">
                    <td class="${ s.student_name}"> ${ s.student_name}</td>
                    <td>${ s.type_score }</td>
                    <td>${ s.score }</td>
                    <td>${ s.class_name }</td>
                    <td>${ s.subject_name }</td>
                    <td>Học kỳ ${ s.semester }, Năm ${ s.year }</td>
                    <td>
                        <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#myModal-update">
                            Sửa
                        </button>
                        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#myModal-delete">
                            Xóa
                        </button>
                    </td>
                </tr>
            `
            let d = document.getElementById("tb-scores")
            d.innerHTML = d.innerHTML + h;
       } else if (data.status == 501)
            alert("Điểm không hợp lệ")
       else if (data.status == 502)
            alert("Lỗi thông tin học sinh (Lớp hoặc học kỳ hoặc năm học không hợp lệ)")
       else
            alert("Lỗi chưa xác định")

    }) // js promise
}