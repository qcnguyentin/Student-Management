from flask_login import current_user

from Stud_Man.models import UserRole


def check_user_role():
    if current_user.is_authenticated:
        if current_user.user_role == UserRole.TEACHER:
            user_role = 1
        elif current_user.user_role == UserRole.EMPLOYEE:
            user_role = 2
        else:
            user_role = 3
    else:
        user_role = 0
    return user_role


def check_list(rep, class_name):
    data = []
    for i in rep:
        if class_name.__eq__(i[0]):
            data.append({
                'tb': i
            })
        elif class_name.__eq__(i[0]):
            data.append({
                'tb': i
            })
    return data


def cal_subject_sem(data, subj, student_id, sem):
    score_avg = []
    count = []
    for i in range(len(subj)):
        count.append(0)
        score_avg.append(0)
    for i in range(len(subj)):
        for s in data:
            if s['tb'][7] == subj[i].name and int(s['tb'][6]) == int(student_id) and int(s['tb'][2]) == sem:
                if s['tb'][5] == "Điểm 1 tiết":
                    score_avg[i] += 2 * s['tb'][1]
                    count[i] += 2
                elif s['tb'][5] == "Điểm 15p":
                    score_avg[i] += s['tb'][1]
                    count[i] += 1
                else:
                    score_avg[i] += 3 * s['tb'][1]
                    count[i] += 3
    for i in range(len(subj)):
        if count[i] == 0:
            count[i] = 1
    score_avg_dv = []
    for i in range(len(subj)):
        score_avg_dv.append(score_avg[i]/count[i])
    return score_avg_dv


#chưa hoàn thành, do tính điểm theo môn chưa hợp lệ
def cal_avg(data, subj):
    stt = 0
    student_id = []
    student_name = []
    student_class_name = []
    score_avg1 = []
    score_avg2 = []
    count = 0
    for s in data:
        if s['tb'][6] not in student_id:
            student_id.append(s['tb'][6])
            student_name.append(s['tb'][4])
            student_class_name.append(s['tb'][0])
            score_avg1.append(0)
            score_avg2.append(0)
    print(score_avg1)
    subject_score_student = []
    id = 0
    for i in student_id:
        subject_score_student.append({
            'id': id,
            'avg_sm1': cal_subject_sem(data, subj, i, 1),
            'avg_sm2': cal_subject_sem(data, subj, i, 2),
        })

        id += 1

    print(subject_score_student)
    for i in subj:
        count += 1

    for i in subject_score_student:
        for j in range(count):
            x = i['id']
            score_avg1[x] += i['avg_sm1'][j]
            score_avg2[x] += i['avg_sm2'][j]


    # danh sách mã học sinh, tên học sinh, lớp

    score = []
    if count == 0:
        count = 1
    for i in range(len(student_id)):
        stt += 1
        score_avg1[i] /= count
        score_avg2[i] /= count

        score.append({
            'stt': stt,
            'student_name': student_name[i],
            'student_class_name': student_class_name[i],
            'score_avg1': round(score_avg1[i], 1),
            'score_avg2': round(score_avg2[i], 1)
        })
    return score
