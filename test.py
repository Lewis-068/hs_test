import streamlit as st

# 1. 현재 화면 상태 및 DB(세션) 초기화
if 'page' not in st.session_state:
    st.session_state['page'] = 'main'  # 기본 화면은 'main'
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = None  # DB에서 조회해온 메일 (없으면 None)

# --------------------------------------------------
# PAGE 1: 메인 화면
# --------------------------------------------------
if st.session_state['page'] == 'main':

    # 1. 상단 자료 탭
    tab1, tab2, tab3 = st.tabs(["수학", "물리", "생명과학"])
    with tab1:
        st.link_button("수학 필기 모음_HS", "https://docs.google.com/...")
    with tab3:
        st.link_button("생물의 유전 '조건 X' 문제", "https://docs.google.com/...")

    # 2. 중단 공지사항
    st.info("📌 **[공지]** 34기 학술 자료실에 오신 것을 환영합니다! 원하는 자료를 선택해 확인하세요.")

    # 3. 하단 좌/우 구역 분할
    col_left, col_right = st.columns(2)

    with col_left:
        # DB에 메일이 있는지 확인하는 조건문
        has_email = st.session_state['user_email'] is not None

        # 체크박스 상태 제어
        agree = st.checkbox("신규 자료 알림 수신 동의", value=has_email)

        if agree and not has_email:
            # 메일이 없는데 체크했으면 메일 등록 창으로 이동!
            st.session_state['page'] = 'email_setting'
            st.rerun()

        if has_email:
            # 메일이 이미 있으면 메일 변경 버튼 노출
            if st.button("메일 변경"):
                st.session_state['page'] = 'email_setting'
                st.rerun()

    with col_right:
        # 익명 건의함 이동 버튼
        if st.button("💬 익명 건의함으로 이동"):
            st.session_state['page'] = 'suggestion'
            st.rerun()

    with st.container(border=True):
        st.markdown("### 📐 수학")
        st.caption("최근 업데이트: 중간고사 대비 통합본")
        st.link_button("자료 열기 ↗", "https://docs.google.com/...", use_container_width=True)

# --------------------------------------------------
# PAGE 2: 익명 건의함 화면
# --------------------------------------------------
elif st.session_state['page'] == 'suggestion':
    st.title("💬 익명 건의함")
    feedback = st.text_area("건의할 내용을 남겨주세요:")

    if st.button("제출"):
        # (구글 시트 등에 저장하는 코드)
        st.success("건의가 접수되었습니다!")

    if st.button("돌아가기"):
        st.session_state['page'] = 'main'
        st.rerun()

# --------------------------------------------------
# PAGE 3: 메일 등록/변경 화면
# --------------------------------------------------
elif st.session_state['page'] == 'email_setting':
    st.title("📧 알림 메일 설정")

    current = st.session_state['user_email']
    st.write(f"현재 등록된 메일: **{current if current else '없음'}**")

    new_email = st.text_input("알림을 받을 이메일을 입력하세요:")

    if st.button("저장"):
        st.session_state['user_email'] = new_email  # DB 저장 처리
        st.success("이메일이 저장되었습니다!")
        st.session_state['page'] = 'main'
        st.rerun()

    if st.button("돌아가기"):
        st.session_state['page'] = 'main'
        st.rerun()
