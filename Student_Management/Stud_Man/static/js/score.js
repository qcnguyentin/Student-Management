function spinner(status="block") {
    let s = document.getElementsByClassName("my-spinner")
    for (let i = 0; i < s.length; i++)
        s[i].style.display = status
}


function addScore(student_id) {
    spinner()
    fetch(`/api/score/${student_id}/score-list`, {
        method: "post",
        body: JSON.stringify({
            'student_name': student_id.name,
            'score': document.getElementById("add-score-score").value,
            'type_score': document.getElementById("add-score-type").value,
            'class_name': document.getElementById("add-score-class").value,
            'semester': document.getElementById("add-score-semester").value,
            'subject_name': document.getElementById("add-score-subject").value,
            'year': document.getElementById("add-score-year").value,
            'student_id': student_id
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => res.json()).then((data) => {
        spinner("none")
       if (data.status === 204) {
            alert("Thêm thành công")
            let i = data.score
            let h = `
                <tr id="score${ i.score_id }">
                    <td style="display: none"><select id="score-id"><option>${ i.score_id }</option></select></td>
                    <td>${ i.score }</td>
                    <td>${ i.type_score }</td>
                    <td>${ i.subject_name }</td>
                    <td>Học kỳ ${ i.semester }, ${ i.year }</td>
                    <td>
                        <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                                data-bs-target="#myModal-update">
                            sửa điểm
                        </button>

                        <input type="submit" value="Xóa điểm" class="btn btn-danger" id="btn-delete-score"
                        onclick="deleteScore(${student_id})"/>
                    </td>
                </tr>
            `
            let d = document.getElementById("tb-score-detail")
            d.innerHTML = h + d.innerHTML;
       } else if (data.status == 501)
            alert("Điểm không hợp lệ")
       else if (data.status == 502)
            alert("Lỗi thông tin học sinh (Lớp hoặc học kỳ hoặc năm học không hợp lệ)")
       else
            alert("Lỗi chưa xác định")
    }) // js promise
}


function deleteScore(student_id) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
         fetch(`/api/score/${student_id}/score-list`, {
             method: "delete",
             body: JSON.stringify({
                'score_id': document.getElementById("score-id").value
             }),
             headers: {
                "Content-Type": "application/json"
            }
         }).then((res) => res.json()).then((data) => {
            data.forEach(s => {
                if(s.status == 204)
                {
                    alert("Xóa thành công")
                    let i = s.score_id
                    console.info(i)
                    let e = document.getElementById(`score${ i }`)
                    console.info(e)
                    e.style.display = "none"
                }
                else
                {
                    alert("Xóa không thành công")
                }
            }) // js promise
         })
    }
}


function updateScore(student_id) {
    if (confirm("Bạn chắc chắn muốn sửa không?") == true) {
         fetch(`/api/score/${student_id}/score-list`, {
             method: "update",
             body: JSON.stringify({
                'score_id': document.getElementById("score-id").value,
                'score_value': document.getElementById("score-update").value
             }),
             headers: {
                "Content-Type": "application/json"
            }
         }).then((res) => res.json()).then((data) => {
            data.forEach(s => {
                if(s.status == 204)
                {
                    alert("Sửa thành công")
                }
                else
                {
                    alert("Sửa không thành công")
                }
            }) // js promise
         })
    }
}


function loadScoresDetail(student_id) {
    spinner()
    fetch(`/api/score/${student_id}/score-list`).then(res => res.json()).then(data => {
        spinner("none")

        let h = "";
        data.forEach(i => {
            h += `
                <tr id="score${ i.score_id }">
                    <td style="display: none"><select id="score-id"><option>${ i.score_id }</option></select></td>
                    <td>${ i.score }</td>
                    <td>${ i.type_score }</td>
                    <td>${ i.subject_name }</td>
                    <td>Học kỳ ${ i.semester }, ${ i.year }</td>
                    <td>
                        <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                                data-bs-target="#myModal-update">
                            sửa điểm
                        </button>

                        <input type="submit" value="Xóa điểm" class="btn btn-danger" id="btn-delete-score"
                        onclick="deleteScore(${student_id})"/>
                    </td>

                </tr>
            `
        })
        let d = document.getElementById("tb-score-detail-body")
        d.innerHTML += h;
    })
}