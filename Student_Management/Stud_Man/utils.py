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
    print(data)
    return data


def cal_avg(data):
    stt = 0
    student_id = []
    student_name = []
    student_class_name = []
    score_avg1 = []
    score_avg2 = []
    count1 = []
    count2 = []
    for s in data:
        if s['tb'][6] not in student_id:
            student_id.append(s['tb'][6])
            score_avg1.append(0)
            score_avg2.append(0)
            student_name.append('')
            student_class_name.append('')
            count1.append(0)
            count2.append(0)
    for s in data:
        if s['tb'][5] == "Điểm 1 tiết":
            for i in range(len(student_id)):
                if s['tb'][6] == student_id[i]:
                    student_name[i] = s['tb'][4]
                    student_class_name[i] = s['tb'][0]
                    if s['tb'][2] == 1:
                        score_avg1[i] += 2 * s['tb'][1]
                        count1[i] += 2
                    else:
                        score_avg2[i] += 2 * s['tb'][1]
                        count2[i] += 2
        elif s['tb'][5] == "Điểm 15p":
            for i in range(len(student_id)):
                if s['tb'][6] == student_id[i]:
                    student_name[i] = s['tb'][4]
                    student_class_name[i] = s['tb'][0]
                    if s['tb'][2] == 1:
                        score_avg1[i] += s['tb'][1]
                        count1[i] += 1
                    else:
                        score_avg2[i] += s['tb'][1]
                        count2[i] += 1
        else:
            for i in range(len(student_id)):
                if s['tb'][6] == student_id[i]:
                    if s['tb'][2] == 1:
                        score_avg1[i] += 3 * s['tb'][1]
                        count1[i] += 3
                    else:
                        score_avg2[i] += 3 * s['tb'][1]
                        count2[i] += 3
                    student_name[i] = s['tb'][4]
                    student_class_name[i] = s['tb'][0]
    score = []
    for i in range(len(student_id)):
        stt += 1
        if count1[i] == 0:
            count1[i] = 1
        if count2[i] == 0:
            count2[i] = 1
        score_avg1[i] /= count1[i]
        score_avg2[i] /= count2[i]
        score.append({
            'stt': stt,
            'student_name': student_name[i],
            'student_class_name': student_class_name[i],
            'score_avg1': score_avg1[i],
            'score_avg2': score_avg2[i]
        })
    return score
