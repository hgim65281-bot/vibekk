import streamlit as st
import random
import math
import html

# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="EVENT:ON",
    page_icon="🎪",
    layout="wide"
)

# =========================================================
# 스타일
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

h1 {
    font-weight: 800;
}

.space-card {
    border: 1px solid #d9d9d9;
    border-radius: 12px;
    padding: 16px;
    background: white;
    margin-bottom: 10px;
}

.sim-card {
    border: 1px solid #d9d9d9;
    border-radius: 12px;
    padding: 15px;
    background: #f8fafc;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 행사 공간 정보
# =========================================================

ELEMENT_INFO = {

    "메인 무대": {
        "icon": "🎤",
        "description": "공연과 발표가 이루어지는 행사의 중심 공간입니다.",
        "benefit": "행사의 중심점을 만들어 참가자의 관심을 집중시키고 프로그램 참여를 유도합니다.",
        "traffic": 0.95
    },

    "체험 부스": {
        "icon": "🧪",
        "description": "참가자가 직접 체험하고 활동하는 공간입니다.",
        "benefit": "참가자의 적극적인 참여를 유도하고 행사 체류 시간을 늘릴 수 있습니다.",
        "traffic": 0.85
    },

    "푸드존": {
        "icon": "🍔",
        "description": "음식과 음료를 이용할 수 있는 공간입니다.",
        "benefit": "장시간 행사에서 참가자의 편의성을 높이고 자연스럽게 휴식 공간 역할도 할 수 있습니다.",
        "traffic": 0.80
    },

    "포토존": {
        "icon": "📸",
        "description": "사진을 촬영할 수 있는 공간입니다.",
        "benefit": "행사의 기억을 남기고 참가자의 자발적인 홍보를 유도할 수 있습니다.",
        "traffic": 0.55
    },

    "휴식 공간": {
        "icon": "🪑",
        "description": "참가자가 앉아서 휴식을 취할 수 있는 공간입니다.",
        "benefit": "장시간 행사에서 피로를 줄이고 참가자의 체류 편의성을 높입니다.",
        "traffic": 0.45
    },

    "화장실": {
        "icon": "🚻",
        "description": "참가자가 이용하는 편의시설입니다.",
        "benefit": "행사장 이용에 필요한 기본 시설로 참가자의 편의성을 높입니다.",
        "traffic": 0.35
    },

    "안내소": {
        "icon": "ℹ️",
        "description": "행사장과 프로그램 정보를 안내하는 공간입니다.",
        "benefit": "참가자의 길찾기와 정보 탐색을 도와 이동 혼란을 줄입니다.",
        "traffic": 0.60
    },

    "응급의료소": {
        "icon": "🏥",
        "description": "응급 상황에 대응하기 위한 공간입니다.",
        "benefit": "응급 상황 발생 시 빠른 대응이 가능하도록 행사장의 안전성을 높입니다.",
        "traffic": 0.15
    },

    "대기 공간": {
        "icon": "⏳",
        "description": "프로그램이나 입장을 기다리는 공간입니다.",
        "benefit": "대기 행렬을 통행로와 분리해 행사장 혼잡을 줄이는 데 도움이 됩니다.",
        "traffic": 0.65
    },

    "굿즈 판매": {
        "icon": "🛍️",
        "description": "행사 관련 상품이나 기념품을 판매하는 공간입니다.",
        "benefit": "행사의 경험을 기념할 수 있도록 하고 추가적인 판매 기회를 제공합니다.",
        "traffic": 0.50
    },

    "장애인 편의시설": {
        "icon": "♿",
        "description": "이동약자의 행사장 이용을 돕는 시설입니다.",
        "benefit": "다양한 참가자가 행사에 편리하게 접근하고 이동할 수 있도록 합니다.",
        "traffic": 0.25
    }
}


# =========================================================
# 행사 종류
# =========================================================

PURPOSES = {

    "축제": [
        "즐거운 체험 제공",
        "지역 홍보",
        "문화·공연 중심",
        "먹거리 중심",
        "가족 참여"
    ],

    "학교 행사": [
        "학생 참여 확대",
        "동아리·진로 체험",
        "공연·발표",
        "학생 교류",
        "축제 분위기 조성"
    ],

    "박람회": [
        "정보 전달",
        "기업·기관 홍보",
        "체험 중심",
        "상담·교류",
        "제품 전시"
    ],

    "공연": [
        "관람객 집중",
        "공연 관람 편의",
        "대기·입장 관리",
        "팬 참여",
        "안전한 관람"
    ],

    "체험 행사": [
        "직접 체험",
        "교육",
        "가족 참여",
        "참여율 증가",
        "체험 대기 관리"
    ],

    "지역 행사": [
        "지역 홍보",
        "주민 참여",
        "관광객 유치",
        "지역 상권 활성화",
        "문화 교류"
    ],

    "전시회": [
        "작품 감상",
        "작품 설명",
        "동선 관리",
        "조용한 관람",
        "체험"
    ],

    "스포츠 행사": [
        "경기 관람",
        "선수·참가자 동선 분리",
        "응원",
        "휴식",
        "안전 관리"
    ]
}


# =========================================================
# 행사별 추천 공간
# =========================================================

RECOMMENDED = {

    "축제": [
        "메인 무대",
        "체험 부스",
        "푸드존",
        "포토존",
        "휴식 공간",
        "화장실",
        "안내소",
        "응급의료소",
        "대기 공간"
    ],

    "학교 행사": [
        "메인 무대",
        "체험 부스",
        "포토존",
        "휴식 공간",
        "화장실",
        "안내소",
        "응급의료소",
        "장애인 편의시설"
    ],

    "박람회": [
        "체험 부스",
        "안내소",
        "휴식 공간",
        "화장실",
        "응급의료소",
        "장애인 편의시설"
    ],

    "공연": [
        "메인 무대",
        "대기 공간",
        "안내소",
        "화장실",
        "응급의료소",
        "휴식 공간",
        "장애인 편의시설"
    ],

    "체험 행사": [
        "체험 부스",
        "대기 공간",
        "안내소",
        "휴식 공간",
        "화장실",
        "응급의료소"
    ],

    "지역 행사": [
        "메인 무대",
        "체험 부스",
        "푸드존",
        "포토존",
        "휴식 공간",
        "화장실",
        "안내소",
        "응급의료소"
    ],

    "전시회": [
        "체험 부스",
        "포토존",
        "휴식 공간",
        "화장실",
        "안내소",
        "장애인 편의시설"
    ],

    "스포츠 행사": [
        "메인 무대",
        "대기 공간",
        "휴식 공간",
        "화장실",
        "안내소",
        "응급의료소",
        "장애인 편의시설"
    ]
}


# =========================================================
# 세션 상태
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = 1

if "design" not in st.session_state:
    st.session_state.design = None

if "selected_space" not in st.session_state:
    st.session_state.selected_space = None


# =========================================================
# 배치도 생성 함수
# =========================================================

def create_layout(selected_spaces):

    """
    모든 공간의 실제 좌표를 생성한다.

    반환값:
    [
        {
            name,
            number,
            x,
            y,
            width,
            height
        }
    ]
    """

    layout = []

    # 행사장 크기
    zone_positions = [

        (8, 10),
        (38, 10),
        (68, 10),

        (8, 30),
        (38, 30),
        (68, 30),

        (8, 50),
        (38, 50),
        (68, 50),

        (8, 67),
        (38, 67),
        (68, 67)

    ]

    position_index = 0

    # 핵심 공간을 먼저 배치
    priority = [

        "안내소",
        "메인 무대",
        "체험 부스",
        "푸드존",
        "포토존",
        "휴식 공간",
        "대기 공간",
        "화장실",
        "응급의료소",
        "굿즈 판매",
        "장애인 편의시설"

    ]

    ordered = sorted(
        selected_spaces.items(),
        key=lambda item:
        priority.index(item[0])
        if item[0] in priority
        else 999
    )

    for name, count in ordered:

        for number in range(1, count + 1):

            if position_index >= len(zone_positions):
                break

            x, y = zone_positions[position_index]

            layout.append({

                "name": name,

                "number": number,

                "x": x,

                "y": y,

                "width": 24,

                "height": 15

            })

            position_index += 1

    return layout


# =========================================================
# 배치도 SVG 생성
# =========================================================

def create_map_svg(layout, show_people=False, people_count=0):

    """
    배치도와 시뮬레이션에서 동일하게 사용하는 SVG.

    핵심:
    시뮬레이션에서도 이 함수에 show_people=True를 넣어서
    '똑같은 배치도' 위에 사람을 추가한다.
    """

    svg = """

    <svg
        viewBox="0 0 100 88"
        width="100%"
        height="auto"
        preserveAspectRatio="xMidYMid meet"
        xmlns="http://www.w3.org/2000/svg"
    >

    <!-- 전체 행사장 -->
    <rect
        x="2"
        y="2"
        width="96"
        height="82"
        rx="3"
        fill="#f8fafc"
        stroke="#1e293b"
        stroke-width="0.8"
    />

    <!-- 제목 -->
    <text
        x="50"
        y="7"
        text-anchor="middle"
        font-size="3.2"
        font-weight="bold"
    >
        EVENT:ON 행사장
    </text>

    <!-- 입구 -->
    <rect
        x="42"
        y="78"
        width="16"
        height="5"
        rx="1"
        fill="#dcfce7"
        stroke="#16a34a"
        stroke-width="0.5"
    />

    <text
        x="50"
        y="81.5"
        text-anchor="middle"
        font-size="2.3"
        font-weight="bold"
    >
        🚪 입구 / 출구
    </text>

    <!-- 주요 통행로 -->
    <path
        d="M50 78
           L50 70
           L20 70
           L20 27
           L50 27
           L50 15"
        fill="none"
        stroke="#94a3b8"
        stroke-width="1.4"
        stroke-dasharray="2 1"
    />

    <path
        d="M50 70
           L80 70
           L80 27
           L50 27"
        fill="none"
        stroke="#94a3b8"
        stroke-width="1.4"
        stroke-dasharray="2 1"
    />

    """


    # -----------------------------------------------------
    # 공간
    # -----------------------------------------------------

    for space in layout:

        name = space["name"]
        number = space["number"]

        x = space["x"]
        y = space["y"]

        width = space["width"]
        height = space["height"]

        info = ELEMENT_INFO.get(
            name,
            {
                "icon": "📌",
                "benefit": "사용자가 직접 추가한 공간입니다."
            }
        )

        icon = info["icon"]

        # 번호
        number_text = ""

        if number > 1:
            number_text = f" {number}"

        safe_name = html.escape(name)

        svg += f"""

        <g>

            <!-- 공간 박스 -->

            <rect
                x="{x}"
                y="{y}"
                width="{width}"
                height="{height}"
                rx="2"
                fill="white"
                stroke="#475569"
                stroke-width="0.7"
            />

            <!-- 아이콘 -->

            <text
                x="{x + width / 2}"
                y="{y + 5}"
                text-anchor="middle"
                font-size="3"
            >
                {icon}
            </text>

            <!-- 공간 이름 -->

            <text
                x="{x + width / 2}"
                y="{y + 9}"
                text-anchor="middle"
                font-size="2.2"
                font-weight="bold"
            >
                {safe_name[:13]}
            </text>

            <!-- 공간 번호 -->

            <text
                x="{x + width / 2}"
                y="{y + 12.5}"
                text-anchor="middle"
                font-size="1.8"
                fill="#64748b"
            >
                {number_text if number > 1 else ""}
            </text>

        </g>

        """


    # -----------------------------------------------------
    # 사람 시뮬레이션
    # -----------------------------------------------------

    if show_people and layout:

        random.seed(2026)

        # 최대 70명의 시각적 에이전트
        visual_people = min(70, max(20, people_count // 10))

        for i in range(visual_people):

            target = random.choice(layout)

            start_x = 50 + random.uniform(-5, 5)
            start_y = 74 + random.uniform(0, 3)

            target_x = (
                target["x"]
                + target["width"] / 2
                + random.uniform(-7, 7)
            )

            target_y = (
                target["y"]
                + target["height"] / 2
                + random.uniform(-4, 4)
            )

            duration = 2.5 + random.uniform(0, 2.5)

            delay = random.uniform(0, 3)

            svg += f"""

            <circle
                cx="{start_x:.2f}"
                cy="{start_y:.2f}"
                r="0.65"
                fill="#334155"
            >

                <animate
                    attributeName="cx"
                    values="{start_x:.2f};
                            50;
                            {target_x:.2f};
                            {target_x:.2f};
                            {start_x:.2f}"
                    dur="{duration:.2f}s"
                    begin="-{delay:.2f}s"
                    repeatCount="indefinite"
                />

                <animate
                    attributeName="cy"
                    values="{start_y:.2f};
                            70;
                            {target_y:.2f};
                            {target_y:.2f};
                            {start_y:.2f}"
                    dur="{duration:.2f}s"
                    begin="-{delay:.2f}s"
                    repeatCount="indefinite"
                />

            </circle>

            """


    svg += """

    <!-- 범례 -->

    <circle
        cx="8"
        cy="86"
        r="1"
        fill="#334155"
    />

    <text
        x="10"
        y="87"
        font-size="1.8"
    >
        사람 이동
    </text>

    <line
        x1="30"
        y1="86"
        x2="38"
        y2="86"
        stroke="#94a3b8"
        stroke-width="1"
        stroke-dasharray="2 1"
    />

    <text
        x="40"
        y="87"
        font-size="1.8"
    >
        주요 이동 동선
    </text>

    </svg>

    """

    return svg


# =========================================================
# PAGE 1
# =========================================================

if st.session_state.page == 1:

    st.title("🎪 EVENT:ON")

    st.caption(
        "사용자의 요구사항을 바탕으로 행사장의 공간 구성과 사람의 이동을 설계합니다."
    )

    st.header("1️⃣ 행사 기본 정보")

    col1, col2 = st.columns(2)

    with col1:

        event_type = st.selectbox(
            "행사장 종류",
            list(PURPOSES.keys())
        )

        purpose = st.selectbox(
            "행사 목적",
            PURPOSES[event_type]
        )

        people = st.number_input(
            "예상 참가 인원",
            min_value=10,
            max_value=100000,
            value=500,
            step=10
        )

        duration = st.number_input(
            "행사 시간",
            min_value=1,
            max_value=24,
            value=4
        )

    with col2:

        age_group = st.selectbox(
            "주요 연령대",
            [
                "어린이 중심",
                "청소년 중심",
                "청년 중심",
                "중장년 중심",
                "고령층 중심",
                "전 연령"
            ]
        )

        atmosphere = st.selectbox(
            "원하는 분위기",
            [
                "활기찬",
                "편안한",
                "가족 친화적",
                "미래지향적",
                "문화적인",
                "고급스러운",
                "친환경적인",
                "역동적인"
            ]
        )

        entrance_fee = st.number_input(
            "예상 입장료",
            min_value=0,
            max_value=1000000,
            value=0,
            step=1000
        )

        venue_type = st.radio(
            "행사장 형태",
            ["실내", "실외"],
            horizontal=True
        )


    # =====================================================
    # 공간 선택
    # =====================================================

    st.divider()

    st.header("2️⃣ 행사장에 넣을 공간")

    st.write(
        f"**{event_type}**에 적합한 공간을 추천했습니다."
    )

    selected = {}

    columns = st.columns(3)

    for i, name in enumerate(RECOMMENDED[event_type]):

        with columns[i % 3]:

            checked = st.checkbox(
                f"{ELEMENT_INFO[name]['icon']} {name}",
                value=True,
                key=f"check_{name}"
            )

            if checked:

                count = st.number_input(
                    f"{name} 개수",
                    min_value=1,
                    max_value=12,
                    value=1,
                    key=f"count_{name}"
                )

                selected[name] = count


    # =====================================================
    # 직접 추가
    # =====================================================

    st.subheader("➕ 직접 추가할 공간")

    custom = st.text_input(
        "공간 이름",
        placeholder="예: VR 체험관, 물품보관소, 상담 부스"
    )

    if custom.strip():

        custom_names = [
            x.strip()
            for x in custom.split(",")
            if x.strip()
        ]

        for item in custom_names:

            count = st.number_input(
                f"{item} 개수",
                min_value=1,
                max_value=12,
                value=1,
                key=f"custom_{item}"
            )

            selected[item] = count


    # =====================================================
    # 설계 시작
    # =====================================================

    st.divider()

    if st.button(
        "✨ 행사장 설계하기",
        type="primary",
        use_container_width=True
    ):

        if not selected:

            st.error(
                "최소 하나 이상의 공간을 선택해주세요."
            )

        elif sum(selected.values()) > 12:

            st.error(
                "현재 버전에서는 배치도에 최대 12개의 공간까지 배치할 수 있습니다."
            )

        else:

            st.session_state.design = {

                "event_type": event_type,
                "purpose": purpose,
                "people": people,
                "duration": duration,
                "age_group": age_group,
                "atmosphere": atmosphere,
                "entrance_fee": entrance_fee,
                "venue_type": venue_type,
                "selected": selected

            }

            st.session_state.selected_space = None

            st.session_state.page = 2

            st.rerun()


# =========================================================
# PAGE 2
# =========================================================

else:

    d = st.session_state.design

    # =====================================================
    # 헤더
    # =====================================================

    st.title("🎪 완성된 행사장")

    st.write(
        f"""
        **{d['event_type']} · {d['purpose']} · {d['people']:,}명 · {d['venue_type']}**
        """
    )


    # =====================================================
    # 면적
    # =====================================================

    area_per_person = 1.8 if d["venue_type"] == "실내" else 2.5

    total_area = max(
        300,
        d["people"] * area_per_person
    )

    st.metric(
        "예상 필요 행사장 면적",
        f"{total_area:,.0f}㎡"
    )


    # =====================================================
    # 배치도 생성
    # =====================================================

    layout = create_layout(
        d["selected"]
    )


    # =====================================================
    # 배치도 + 설명
    # =====================================================

    left, right = st.columns(
        [3.5, 1.3]
    )

    with left:

        st.subheader("🗺️ 행사장 배치도")

        st.caption(
            "배치도에 포함된 공간을 선택하면 오른쪽에서 해당 공간의 역할과 장점을 확인할 수 있습니다."
        )

        map_svg = create_map_svg(
            layout,
            show_people=False
        )

        st.components.v1.html(
            map_svg,
            height=750,
            scrolling=False
        )


    with right:

        st.subheader("📌 공간 설명")

        names = list(d["selected"].keys())

        if st.session_state.selected_space is None:

            st.session_state.selected_space = names[0]


        for name in names:

            info = ELEMENT_INFO.get(
                name,
                {
                    "icon": "📌",
                    "description": "사용자가 직접 추가한 공간입니다.",
                    "benefit": "행사 목적에 맞게 활용할 수 있습니다."
                }
            )

            if st.button(
                f"{info['icon']} {name}",
                key=f"space_info_{name}",
                use_container_width=True
            ):

                st.session_state.selected_space = name


        selected_name = st.session_state.selected_space

        info = ELEMENT_INFO.get(
            selected_name,
            {
                "icon": "📌",
                "description": "사용자가 직접 추가한 공간입니다.",
                "benefit": "행사 목적에 맞게 활용할 수 있습니다."
            }
        )

        st.markdown(
            f"""
            <div class="space-card">

            <h3>
            {info['icon']} {selected_name}
            </h3>

            <b>역할</b>

            <p>
            {info['description']}
            </p>

            <b>장점</b>

            <p>
            {info['benefit']}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # 시뮬레이션
    # =====================================================

    st.divider()

    st.header("4️⃣ 사람 이동 시뮬레이션")

    st.write(
        "⚠️ 아래 시뮬레이션은 **위에서 생성된 동일한 배치도 위에 사람의 이동을 표시**합니다."
    )


    # =====================================================
    # 공간별 예상 방문량 계산
    # =====================================================

    traffic_scores = {}

    for space in layout:

        name = space["name"]

        info = ELEMENT_INFO.get(
            name,
            {
                "traffic": 0.4
            }
        )

        base = info["traffic"]

        # 행사 목적에 따른 추가 가중치
        if d["purpose"] in [
            "문화·공연 중심",
            "공연·발표",
            "관람객 집중"
        ]:

            if name == "메인 무대":
                base *= 1.5

        if d["purpose"] in [
            "즐거운 체험 제공",
            "직접 체험",
            "체험 중심",
            "동아리·진로 체험"
        ]:

            if name == "체험 부스":
                base *= 1.5

        if d["purpose"] in [
            "먹거리 중심"
        ]:

            if name == "푸드존":
                base *= 1.5

        traffic_scores[name] = traffic_scores.get(
            name,
            0
        ) + base


    # 가장 많이 모일 공간
    hotspot = max(
        traffic_scores,
        key=traffic_scores.get
    )


    max_score = max(
        traffic_scores.values()
    )


    # =====================================================
    # 혼잡도
    # =====================================================

    crowd_value = (
        d["people"]
        /
        max(
            1,
            len(layout) * 45
        )
    )

    crowd_score = min(
        100,
        int(
            crowd_value
            *
            traffic_scores[hotspot]
            *
            25
        )
    )


    # =====================================================
    # 정보 카드
    # =====================================================

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "예상 참가자",
        f"{d['people']:,}명"
    )

    m2.metric(
        "가장 많이 모일 것으로 예상되는 공간",
        hotspot
    )

    m3.metric(
        "예상 최대 혼잡도",
        f"{crowd_score}/100"
    )


    # =====================================================
    # 같은 배치도 + 사람
    # =====================================================

    st.subheader("👥 실제 배치도 위에서 보는 사람 이동")

    simulation_svg = create_map_svg(
        layout,
        show_people=True,
        people_count=d["people"]
    )

    st.components.v1.html(
        simulation_svg,
        height=750,
        scrolling=False
    )


    # =====================================================
    # 공간별 예상 방문량
    # =====================================================

    st.subheader("📊 공간별 예상 집중도")

    total_score = sum(
        traffic_scores.values()
    )

    for name, score in sorted(
        traffic_scores.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        percentage = (
            score
            /
            total_score
            *
            100
        )

        st.write(
            f"**{name}** — 예상 이동 비중 {percentage:.1f}%"
        )

        st.progress(
            min(
                1.0,
                percentage / 100
            )
        )


    # =====================================================
    # 혼잡 분석
    # =====================================================

    st.subheader("🚨 혼잡 분석")

    if crowd_score >= 70:

        st.error(
            f"🔴 **{hotspot}**에 사람이 집중될 가능성이 높습니다."
        )

        st.write(
            "대기 공간을 추가하거나 해당 공간 주변의 이동 통로를 넓히는 방법을 고려할 수 있습니다."
        )

    elif crowd_score >= 40:

        st.warning(
            f"🟠 **{hotspot}** 주변에 참가자가 어느 정도 집중될 것으로 예상됩니다."
        )

        st.write(
            "행사 진행 중 해당 공간의 대기열과 통행로를 관리하는 것이 좋습니다."
        )

    else:

        st.success(
            f"🟢 현재 조건에서는 참가자의 이동이 비교적 분산될 것으로 예상됩니다."
        )


    # =====================================================
    # 다시 설계
    # =====================================================

    st.divider()

    if st.button(
        "← 입력값 수정하기",
        use_container_width=True
    ):

        st.session_state.page = 1

        st.session_state.selected_space = None

        st.rerun()


    st.caption(
        "※ 사람 이동은 입력된 참가 인원, 행사 목적, 공간 구성에 따른 프로토타입 예측입니다. "
        "실제 행사장의 군중 이동을 측정한 결과는 아닙니다."
    )
