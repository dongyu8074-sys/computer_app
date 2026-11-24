import streamlit as st

# 1. 일일 사용 시간대별 상태 안내 함수 (if-elif-else 활용)
def check_usage_status(hours):
    if hours >= 6:
        return "🚨 화면을 끄고 휴식하는 것이 필요합니다."
    elif hours >= 3:
        return "⚠️ 계속 사용해도 괜찮습니다. (단, 눈 피로 방지를 위해 잠시 스트레칭을 권장합니다.)"
    else:
        return "✅ 계속 사용해도 괜찮습니다."

# 2. 주간 사용 시간 분석 및 권장 시간 계산 함수
def analyze_weekly_plan(usage_list):
    max_weekly_hours = 36.0  # 일주일 최대 권장 사용 시간
    days_passed = len(usage_list)
    remaining_days = 7 - days_passed
    
    total_used = sum(usage_list)
    avg_used = total_used / days_passed
    remaining_hours = max_weekly_hours - total_used
    
    return total_used, avg_used, remaining_days, remaining_hours

# 3. 주간 사용 시간 기반 이용 수준(상/중/하) 분류 함수 (적게 사용할수록 '상')
def classify_usage_level(total_hours):
    if total_hours < 18.0:
        return "상 (우수 관리)", "주간 사용 시간이 18시간 미만으로, 피로도를 매우 건강하게 관리하고 있습니다."
    elif total_hours <= 36.0:
        return "중 (적정 관리)", "주간 사용 시간이 권장 한도(36시간) 이내로 적절하게 유지되고 있습니다."
    else:
        return "하 (관리 필요)", "주간 사용 시간이 최대 권장 시간(36시간)을 초과했습니다. 휴식이 시급합니다."

# --- Streamlit 화면 구성 ---
st.title("💻 컴퓨터 사용 피로도 & 주간 시간 관리기")
st.write("오늘까지의 컴퓨터 사용 시간을 입력하고 건강한 사용 계획을 확인해 보세요.")

# 요일 리스트 및 오늘 요일 선택
days_of_week = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
today = st.selectbox("오늘의 요일을 선택하세요:", days_of_week)
today_index = days_of_week.index(today)

st.subheader(f"📅 월요일부터 {today}까지의 사용 시간 입력 (단위: 시간)")

# 4. 반복문(for)을 사용하여 월요일부터 선택한 요일까지 입력창 생성
daily_usages = []
for i in range(today_index + 1):
    day_name = days_of_week[i]
    hours = st.number_input(
        f"{day_name} 사용 시간", 
        min_value=0.0, 
        max_value=24.0, 
        value=0.0, 
        step=0.5,
        key=f"day_{i}"
    )
    daily_usages.append(hours)

# 5. '분석하기' 버튼 및 결과 출력
if st.button("분석하기"):
    st.divider()
    
    # 오늘(가장 마지막에 입력한 요일)의 사용 시간 기준 상태 출력
    today_hours = daily_usages[-1]
    status_message = check_usage_status(today_hours)
    
    st.subheader(f"🔍 오늘({today}) 사용 시간 진단 ({today_hours}시간)")
    if today_hours >= 6:
        st.error(status_message)
    else:
        st.success(status_message)
        
    # 요일별 상태 요약 (for 반복문 활용)
    with st.expander("요일별 상세 진단 내역 보기"):
        for i in range(len(daily_usages)):
            st.write(f"- **{days_of_week[i]}** ({daily_usages[i]}시간): {check_usage_status(daily_usages[i])}")

    # 주간 평균, 이용 수준 등급 및 향후 권장 사용 시간 분석
    total_used, avg_used, remaining_days, remaining_hours = analyze_weekly_plan(daily_usages)
    usage_level, level_desc = classify_usage_level(total_used)
    
    st.subheader("📊 주간 사용량 및 이용 수준 분석")
    col1, col2, col3 = st.columns(3)
    col1.metric("현재까지 누적 시간", f"{total_used:.1f} 시간")
    col2.metric("일일 평균 시간", f"{avg_used:.1f} 시간")
    col3.metric("이용 수준 등급", usage_level)
    
    st.caption(f"📌 등급 안내: {level_desc}")
    
    if remaining_days > 0:
        if remaining_hours > 0:
            daily_recommended = remaining_hours / remaining_days
            st.info(f"💡 일주일 권장 한도(36시간) 기준, **앞으로 {remaining_days}일간 하루 평균 {daily_recommended:.1f}시간 정도까지 사용하는 것이 좋겠습니다.** (총 잔여 권장 시간: {remaining_hours:.1f}시간)")
        else:
            st.warning(f"⚠️ 이미 일주일 최대 권장 시간(36시간)을 {abs(remaining_hours):.1f}시간 초과했습니다. **앞으로 {remaining_days}일간은 컴퓨터 사용을 최소화하고 충분한 휴식을 취하세요.**")
    else:
        # 일요일까지 모두 입력한 경우
        if remaining_hours >= 0:
            st.success(f"🎉 이번 주 총 {total_used:.1f}시간을 사용하여 권장 시간(36시간) 이내로 잘 관리하셨습니다!")
        else:
            st.warning(f"⚠️ 이번 주 총 {total_used:.1f}시간을 사용하여 권장 시간(36시간)을 초과했습니다. 다음 주에는 사용 시간을 줄여보세요.")
