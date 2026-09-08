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
#
# base_area = 기본 필요 면적
# min_area = 최소 면적
# area_per_person = 참가자 증가에 따른 추가 면적
# =========================================================

ELEMENT_INFO = {

    "메인 무대": {
        "icon": "🎤",
        "base_area": 100,
        "min_area": 80,
        "area_per_person": 0.08,
        "description": "공연과 발표가 이루어지는 행사의 중심 공간입니다.",
        "benefit": "행사의 중심점을 만들어 참가자의 관심을 집중시키고 프로그램 참여를 유도합니다.",
        "traffic": 0.95
    },

    "체험 부스": {
        "icon": "🧪",
        "base_area": 9,
        "min_area": 9,
        "area_per_person": 0,
        "description": "참가자가 직접 체험하고 활동하는 공간입니다.",
        "benefit": "참가자의 적극적인 참여를 유도하고 행사 체류 시간을 늘릴 수 있습니다.",
        "traffic": 0.85
    },

    "대형 체험 부스": {
        "icon": "🏗️",
        "base_area": 20,
        "min_area": 20,
        "area_per_person": 0,
        "description": "여러 명이 동시에 참여할 수 있는 대형 체험 공간입니다.",
        "benefit": "인기 체험 프로그램에서 동시에 많은 참가자를 수용할 수 있습니다.",
        "traffic": 0.90
    },

    "푸드존": {
        "icon": "🍔",
        "base_area": 40,
        "min_area": 35,
        "area_per_person": 0.03,
        "description": "음식과 음료를 이용할 수 있는 공간입니다.",
        "benefit": "장시간 행사에서 참가자의 편의성을 높이고 자연스럽게 휴식 공간 역할도 할 수 있습니다.",
        "traffic": 0.80
    },

    "포토존": {
        "icon": "📸",
        "base_area": 15,
        "min_area": 12,
        "area_per_person": 0,
        "description": "사진을 촬영할 수 있는 공간입니다.",
        "benefit": "행사의 기억을 남기고 참가자의 자발적인 홍보를 유도할 수 있습니다.",
        "traffic": 0.55
    },

    "휴식 공간": {
        "icon": "🪑",
        "base_area": 25,
        "min_area": 20,
        "area_per_person": 0.02,
        "description": "참가자가 앉아서 휴식을 취할 수 있는 공간입니다.",
        "benefit": "장시간 행사에서 피로를 줄이고 참가자의 체류 편의성을 높입니다.",
        "traffic": 0.45
    },

    "화장실": {
        "icon": "🚻",
        "base_area": 20,
        "min_area": 15,
        "area_per_person": 0.015,
        "description": "참가자가 이용하는 편의시설입니다.",
        "benefit": "행사장 이용에 필요한 기본 시설로 참가자의 편의성을 높입니다.",
        "traffic": 0.35
    },

    "안내소": {
        "icon": "ℹ️",
        "base_area": 12,
        "min_area": 10,
        "area_per_person": 0,
        "description": "행사장과 프로그램 정보를 안내하는 공간입니다.",
        "benefit": "참가자의 길찾기와 정보 탐색을 도와 이동 혼란을 줄입니다.",
        "traffic": 0.60
    },

    "응급의료소": {
        "icon": "🏥",
        "base_area": 18,
        "min_area": 15,
        "area_per_person": 0,
        "description": "응급 상황에 대응하기 위한 공간입니다.",
        "benefit": "응급 상황 발생 시 빠른 대응이 가능하도록 행사장의 안전성을 높입니다.",
        "traffic": 0.15
    },

    "대기 공간": {
        "icon": "⏳",
        "base_area": 30,
        "min_area": 20,
        "area_per_person": 0.03,
        "description": "프로그램이나 입장을 기다리는 공간입니다.",
        "benefit": "대기 행렬을 통행로와 분리해 행사장 혼잡을 줄이는 데 도움이 됩니다.",
        "traffic": 0.65
    },

    "굿즈 판매": {
        "icon": "🛍️",
        "base_area": 18,
        "min_area": 12,
        "area_per_person": 0.01,
        "description": "행사 관련 상품이나 기념품을 판매하는 공간입니다.",
        "benefit": "행사의 경험을 기념할 수 있도록 하고 추가적인 판매 기회를 제공합니다.",
        "traffic": 0.50
    },

    "장애인 편의시설": {
        "icon": "♿",
        "base_area": 20,
        "min_area": 15,
        "area_per_person": 0.01,
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
        "대형 체험 부스",
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
        "대형 체험 부스",
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
# 공간 실제 면적 계산
# =========================================================

def calculate_space_area(name, people):

    info = ELEMENT_INFO.get(name)

    if info is None:

        # 직접 추가 공간
        return max(
            12,
            12 + int(people * 0.005)
        )

    area = (
        info["base_area"]
        +
        people * info["area_per_person"]
    )

    return max(
        info["min_area"],
        round(area, 1)
    )


# =========================================================
# 행사장 전체 필요 면적
# =========================================================

def calculate_venue_area(
    people,
    venue_type
):

    if venue_type == "실내":

        per_person = 1.8

    else:

        per_person = 2.5

    return max(
        300,
        people * per_person
    )


# =========================================================
# 실제 크기를 바탕으로 직사각형 크기 계산
# =========================================================

def get_rectangle_size(area):

    # 실제 공간을 너무 길쭉하게 만들지 않도록
    # 가로:세로 약 1.5:1
    ratio = 1.5

    width = math.sqrt(
        area * ratio
    )

    height = area / width

    return width, height


# =========================================================
# 실제 행사장 배치 생성
#
# 핵심:
# - 공간마다 크기 다름
# - 최대 12개 제한 없음
# - 공간 사이에 통로 확보
# - 큰 공간부터 먼저 배치
# =========================================================

def create_realistic_layout(
    selected_spaces,
    people,
    venue_area
):

    venue_width = math.sqrt(
        venue_area * 1.5
    )

    venue_height = (
        venue_area / venue_width
    )

    # 행사장 외곽 여백
    margin = 5

    # 통로 폭
    corridor = 4

    usable_width = (
        venue_width
        -
        margin * 2
    )

    # -----------------------------------------------------
    # 공간 하나하나 실제 크기 계산
    # -----------------------------------------------------

    spaces = []

    for name, count in selected_spaces.items():

        for number in range(
            1,
            count + 1
        ):

            area = calculate_space_area(
                name,
                people
            )

            width, height = (
                get_rectangle_size(area)
            )

            spaces.append({

                "name": name,

                "number": number,

                "area": area,

                "width": width,

                "height": height

            })


    # -----------------------------------------------------
    # 큰 공간 먼저 배치
    # -----------------------------------------------------

    spaces.sort(
        key=lambda x: x["area"],
        reverse=True
    )


    # -----------------------------------------------------
    # 여러 줄로 자동 배치
    # -----------------------------------------------------

    rows = []

    current_row = []

    current_width = 0

    current_height = 0


    for space in spaces:

        needed_width = (
            space["width"]
            +
            corridor
        )

        # 현재 행에 공간이 들어가지 않으면
        # 다음 행으로 이동
        if (
            current_row
            and
            current_width + needed_width
            >
            usable_width
        ):

            rows.append({

                "spaces": current_row,

                "height": current_height

            })

            current_row = []

            current_width = 0

            current_height = 0


        current_row.append(space)

        current_width += needed_width

        current_height = max(
            current_height,
            space["height"]
        )


    if current_row:

        rows.append({

            "spaces": current_row,

            "height": current_height

        })


    # -----------------------------------------------------
    # 실제 좌표 생성
    # -----------------------------------------------------

    layout = []

    y = margin + 8


    for row_index, row in enumerate(rows):

        x = margin

        row_height = row["height"]


        for space in row["spaces"]:

            layout.append({

                "name": space["name"],

                "number": space["number"],

                "area": space["area"],

                "x": x,

                "y": y,

                "width": space["width"],

                "height": space["height"],

                "row": row_index

            })

            x += (
                space["width"]
                +
                corridor
            )


        y += (
            row_height
            +
            corridor
        )


    # -----------------------------------------------------
    # 행사장 높이에 맞춰 자동 축소
    # -----------------------------------------------------

    used_height = y + margin


    if used_height > venue_height:

        scale = (
            venue_height
            -
            margin * 2
        ) / max(
            used_height - margin,
            1
        )


        for item in layout:

            item["x"] *= scale
            item["y"] *= scale

            item["width"] *= scale
            item["height"] *= scale

            item["area"] = round(
                item["area"] * scale * scale,
                1
            )


    return (
        layout,
        venue_width,
        venue_height
    )


# =========================================================
# 공간에 가장 가까운 통로 위치 찾기
# =========================================================

def get_space_corridor_point(
    space,
    venue_width,
    venue_height
):

    center_x = (
        space["x"]
        +
        space["width"] / 2
    )

    center_y = (
        space["y"]
        +
        space["height"] / 2
    )

    main_corridor_x = (
        venue_width / 2
    )


    # 중앙 통로에서 가까운 쪽을
    # 해당 공간의 출입구로 사용

    if center_x < main_corridor_x:

        door_x = (
            space["x"]
            +
            space["width"]
        )

    else:

        door_x = space["x"]


    return (
        door_x,
        center_y
    )


# =========================================================
# 두 공간 사이 이동 경로
#
# 부스를 관통하지 않음
# =========================================================

def create_walk_path(
    start_space,
    end_space,
    venue_width,
    venue_height
):

    center_x = (
        venue_width / 2
    )

    # 시작 공간 출입구
    start_door = get_space_corridor_point(
        start_space,
        venue_width,
        venue_height
    )

    # 목적 공간 출입구
    end_door = get_space_corridor_point(
        end_space,
        venue_width,
        venue_height
    )


    # 입구/통로 기준으로 움직임
    path = [

        start_door,

        (
            center_x,
            start_door[1]
        ),

        (
            center_x,
            end_door[1]
        ),

        end_door

    ]


    return path


# =========================================================
# SVG
# =========================================================

def create_map_svg(
    layout,
    venue_width,
    venue_height,
    show_people=False,
    people_count=0
):

    # SVG 내부는 고정 비율
    SVG_W = 120
    SVG_H = 90


    def sx(value):

        return (
            value
            /
            venue_width
            *
            SVG_W
        )


    def sy(value):

        return (
            value
            /
            venue_height
            *
            SVG_H
        )


    def sw(value):

        return (
            value
            /
            venue_width
            *
            SVG_W
        )


    def sh(value):

        return (
            value
            /
            venue_height
            *
            SVG_H
        )


    svg = f"""
    <svg
        viewBox="0 0 {SVG_W} {SVG_H}"
        width="100%"
        height="auto"
        preserveAspectRatio="xMidYMid meet"
        xmlns="http://www.w3.org/2000/svg"
    >

    <!-- 행사장 -->
    <rect
        x="1"
        y="1"
        width="118"
        height="88"
        rx="3"
        fill="#f8fafc"
        stroke="#1e293b"
        stroke-width="0.8"
    />

    <!-- 제목 -->
    <text
        x="60"
        y="5"
        text-anchor="middle"
        font-size="3"
        font-weight="bold"
    >
        EVENT:ON 행사장 배치도
    </text>

    """


    # =====================================================
    # 중앙 메인 통로
    # =====================================================

    center_x = sx(
        venue_width / 2
    )


    svg += f"""

    <!-- 중앙 통로 -->
    <rect
        x="{center_x - 2.2}"
        y="7"
        width="4.4"
        height="76"
        rx="1"
        fill="#e5e7eb"
    />

    """


    # =====================================================
    # 가로 연결 통로
    #
    # 각 행의 공간 앞을 연결
    # =====================================================

    row_centers = {}


    for item in layout:

        row = item["row"]

        center_y = (
            item["y"]
            +
            item["height"] / 2
        )

        if row not in row_centers:

            row_centers[row] = center_y


    for row, y in row_centers.items():

        svg += f"""

        <rect
            x="3"
            y="{sy(y) - 1.8}"
            width="114"
            height="3.6"
            rx="1"
            fill="#e5e7eb"
        />

        """


    # =====================================================
    # 입구 / 출구
    # =====================================================

    svg += """

    <rect
        x="51"
        y="82"
        width="18"
        height="6"
        rx="1"
        fill="#dcfce7"
        stroke="#16a34a"
        stroke-width="0.5"
    />

    <text
        x="60"
        y="86"
        text-anchor="middle"
        font-size="2.2"
        font-weight="bold"
    >
        🚪 입구 / 출구
    </text>

    """


    # =====================================================
    # 공간 그리기
    # =====================================================

    for item in layout:

        x = sx(item["x"])
        y = sy(item["y"])

        width = sw(item["width"])
        height = sh(item["height"])

        name = html.escape(
            item["name"]
        )

        info = ELEMENT_INFO.get(
            item["name"],
            {
                "icon": "📦"
            }
        )

        icon = info["icon"]


        # 면적별 시각 구분
        if item["area"] >= 80:

            fill = "#dbeafe"

        elif item["area"] >= 30:

            fill = "#dcfce7"

        else:

            fill = "#fef3c7"


        # 공간 박스
        svg += f"""

        <rect
            x="{x}"
            y="{y}"
            width="{width}"
            height="{height}"
            rx="1.5"
            fill="{fill}"
            stroke="#334155"
            stroke-width="0.55"
        />

        """


        # 아이콘
        svg += f"""

        <text
            x="{x + width / 2}"
            y="{y + height / 2 - 1}"
            text-anchor="middle"
            font-size="3"
        >
            {icon}
        </text>

        """


        # 이름
        svg += f"""

        <text
            x="{x + width / 2}"
            y="{y + height / 2 + 2.5}"
            text-anchor="middle"
            font-size="2"
            font-weight="bold"
        >
            {name[:14]}
        </text>

        """


        # 면적
        svg += f"""

        <text
            x="{x + width / 2}"
            y="{y + height / 2 + 5}"
            text-anchor="middle"
            font-size="1.6"
            fill="#64748b"
        >
            {item['area']:.1f}㎡
        </text>

        """


    # =====================================================
    # 사람 이동 시뮬레이션
    #
    # 중요:
    # 공간을 직접 통과하지 않는다.
    #
    # 반드시
    # 공간 출입구
    # → 중앙 통로
    # → 목적 공간 출입구
    #
    # 순서로 이동
    # =====================================================

    if show_people and layout:

        random.seed(20260908)

        visual_people = min(
            80,
            max(
                20,
                people_count // 10
            )
        )


        for i in range(
            visual_people
        ):

            # 출발 공간
            start_space = random.choice(
                layout
            )

            # 목적 공간
            end_space = random.choice(
                layout
            )


            # 입구에서 시작하는 경우
            start_x = (
                venue_width / 2
            )

            start_y = (
                venue_height
                - 5
            )


            # 목적지 출입구
            end_door = (
                get_space_corridor_point(
                    end_space,
                    venue_width,
                    venue_height
                )
            )


            # 실제 통로를 따라 이동
            path = [

                (
                    start_x,
                    start_y
                ),

                (
                    venue_width / 2,
                    end_door[1]
                ),

                end_door

            ]


            # SVG path
            path_string = ""

            for index, point in enumerate(
                path
            ):

                px = sx(point[0])
                py = sy(point[1])

                if index == 0:

                    path_string += (
                        f"M {px:.2f} {py:.2f} "
                    )

                else:

                    path_string += (
                        f"L {px:.2f} {py:.2f} "
                    )


            duration = (
                4
                +
                random.random() * 3
            )

            delay = (
                i * 0.12
            )


            svg += f"""

            <circle
                r="0.65"
                fill="#334155"
                opacity="0.75"
            >

                <animateMotion
                    dur="{duration:.2f}s"
                    begin="-{delay:.2f}s"
                    repeatCount="indefinite"
                    path="{path_string}"
                />

            </circle>

            """


    # =====================================================
    # 범례
    # =====================================================

    svg += """

    <circle
        cx="8"
        cy="86"
        r="1"
        fill="#334155"
    />

    <text
        x="11"
        y="87"
        font-size="1.8"
    >
        사람 이동
    </text>

    <rect
        x="35"
        y="85"
        width="5"
        height="2"
        fill="#e5e7eb"
    />

    <text
        x="42"
        y="87"
        font-size="1.8"
    >
        통로
    </text>

    </svg>

    """


    return svg


# =========================================================
# 혼잡도 계산
# =========================================================

def calculate_crowding(
    people,
    duration
):

    density = (
        people
        /
        max(duration, 1)
    )


    if density < 100:

        return "낮음"

    elif density < 250:

        return "보통"

    elif density < 500:

        return "높음"

    else:

        return "매우 높음"


# =========================================================
# 로그인
# =========================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = True


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

    st.info(
        "각 공간은 실제 필요한 면적을 다르게 계산합니다. "
        "필요하지 않은 공간은 0개로 설정할 수 있습니다."
    )


    selected = {}


    columns = st.columns(3)


    for i, name in enumerate(
        RECOMMENDED[event_type]
    ):

        with columns[i % 3]:

            info = ELEMENT_INFO[name]


            st.markdown(
                f"### {info['icon']} {name}"
            )


            preview_area = calculate_space_area(
                name,
                people
            )


            st.caption(
                f"예상 기본 면적: 약 {preview_area:.1f}㎡"
            )


            count = st.number_input(
                f"{name} 개수",
                min_value=0,
                max_value=100,
                value=1,
                step=1,
                key=f"count_{event_type}_{name}"
            )


            # 0개도 저장
            selected[name] = count


    # =====================================================
    # 직접 추가
    # =====================================================

    st.divider()

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
                min_value=0,
                max_value=100,
                value=1,
                step=1,
                key=f"custom_{item}"
            )


            selected[item] = count


            # 직접 추가한 공간 정보
            if item not in ELEMENT_INFO:

                ELEMENT_INFO[item] = {

                    "icon": "📦",

                    "base_area": 12,

                    "min_area": 8,

                    "area_per_person": 0,

                    "description":
                        "사용자가 직접 추가한 행사 공간입니다.",

                    "benefit":
                        "행사 목적에 맞게 자유롭게 구성할 수 있습니다.",

                    "traffic": 0.50

                }


    # =====================================================
    # 설계 시작
    # =====================================================

    st.divider()


    if st.button(
        "✨ 행사장 설계하기",
        type="primary",
        use_container_width=True
    ):

        # 0개인 공간 제거
        final_selected = {

            name: count

            for name, count
            in selected.items()

            if count > 0

        }


        if not final_selected:

            st.error(
                "최소 하나 이상의 공간을 1개 이상 설정해주세요."
            )


        else:

            venue_area = calculate_venue_area(
                people,
                venue_type
            )


            layout, venue_width, venue_height = (
                create_realistic_layout(
                    final_selected,
                    people,
                    venue_area
                )
            )


            st.session_state.design = {

                "event_type":
                    event_type,

                "purpose":
                    purpose,

                "people":
                    people,

                "duration":
                    duration,

                "age_group":
                    age_group,

                "atmosphere":
                    atmosphere,

                "entrance_fee":
                    entrance_fee,

                "venue_type":
                    venue_type,

                "selected":
                    final_selected,

                "layout":
                    layout,

                "venue_area":
                    venue_area,

                "venue_width":
                    venue_width,

                "venue_height":
                    venue_height

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
    # 기본 정보
    # =====================================================

    st.title("🎪 완성된 행사장")


    st.write(
        f"""
        **{d['event_type']} ·
        {d['purpose']} ·
        {d['people']:,}명 ·
        {d['venue_type']}**
        """
    )


    # =====================================================
    # 면적 / 공간 수
    # =====================================================

    total_area = d["venue_area"]

    actual_space_count = len(
        d["layout"]
    )


    m1, m2, m3 = st.columns(3)


    m1.metric(
        "예상 행사장 면적",
        f"{total_area:,.0f}㎡"
    )


    m2.metric(
        "실제 배치 공간",
        f"{actual_space_count}개"
    )


    m3.metric(
        "예상 혼잡도",
        calculate_crowding(
            d["people"],
            d["duration"]
        )
    )


    # =====================================================
    # 배치도
    # =====================================================

    st.divider()

    st.subheader("🗺️ 실제 행사장 배치도")


    st.caption(
        "공간마다 실제 필요 면적을 다르게 계산하고, 공간 사이에 통행로를 확보하여 자동 배치했습니다."
    )


    layout = d["layout"]


    map_svg = create_map_svg(
        layout,
        d["venue_width"],
        d["venue_height"],
        show_people=False
    )


    st.components.v1.html(
        map_svg,
        height=750,
        scrolling=False
    )


    # =====================================================
    # 공간 상세
    # =====================================================

    st.divider()

    st.subheader("🔎 공간 상세 정보")


    if layout:

        space_options = []


        for index, item in enumerate(
            layout
        ):

            space_options.append(
                f"{ELEMENT_INFO.get(item['name'], {}).get('icon', '📦')} "
                f"{item['name']} #{item['number']} "
                f"— {item['area']:.1f}㎡"
            )


        selected_label = st.selectbox(
            "확인할 공간을 선택하세요",
            space_options
        )


        selected_index = (
            space_options.index(
                selected_label
            )
        )


        selected_item = layout[
            selected_index
        ]


        info = ELEMENT_INFO.get(
            selected_item["name"],
            {
                "icon": "📦",
                "description":
                    "사용자가 직접 추가한 공간입니다.",
                "benefit":
                    "행사 목적에 맞게 활용할 수 있습니다."
            }
        )


        st.markdown(
            f"""
            <div class="space-card">

            <h3>
            {info['icon']} {selected_item['name']} #{selected_item['number']}
            </h3>

            <b>실제 배정 면적</b>

            <p>
            {selected_item['area']:.1f}㎡
            </p>

            <b>예상 크기</b>

            <p>
            {selected_item['width']:.1f}m ×
            {selected_item['height']:.1f}m
            </p>

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
    # 공간별 크기
    # =====================================================

    st.divider()

    st.subheader("📐 공간별 실제 크기")


    for item in layout:

        st.write(
            f"**{item['name']} #{item['number']}** "
            f"→ {item['area']:.1f}㎡ "
            f"({item['width']:.1f}m × "
            f"{item['height']:.1f}m)"
        )


    # =====================================================
    # 시뮬레이션
    # =====================================================

    st.divider()

    st.header("🚶 사람 이동 시뮬레이션")


    st.info(
        "⚠️ 위에서 생성된 배치도와 **동일한 공간 좌표**를 사용합니다. "
        "사람은 부스 내부를 통과하지 않고 통로를 따라 이동합니다."
    )


    # =====================================================
    # 시뮬레이션 SVG
    # =====================================================

    simulation_svg = create_map_svg(
        layout,
        d["venue_width"],
        d["venue_height"],
        show_people=True,
        people_count=d["people"]
    )


    st.components.v1.html(
        simulation_svg,
        height=750,
        scrolling=False
    )


    # =====================================================
    # 공간별 혼잡도
    # =====================================================

    st.subheader("📊 공간별 예상 집중도")


    traffic_scores = {}


    for item in layout:

        name = item["name"]


        info = ELEMENT_INFO.get(
            name,
            {
                "traffic": 0.5
            }
        )


        score = info["traffic"]


        # 행사 목적에 따라 가중치 적용

        if d["purpose"] in [
            "문화·공연 중심",
            "공연·발표",
            "관람객 집중"
        ]:

            if name == "메인 무대":

                score *= 1.5


        if d["purpose"] in [
            "즐거운 체험 제공",
            "직접 체험",
            "체험 중심",
            "동아리·진로 체험"
        ]:

            if name in [
                "체험 부스",
                "대형 체험 부스"
            ]:

                score *= 1.5


        if d["purpose"] == "먹거리 중심":

            if name == "푸드존":

                score *= 1.5


        # 면적이 작을수록 같은 인원이 몰릴 때
        # 혼잡도가 올라가도록 계산

        density = (
            d["people"]
            /
            max(
                item["area"],
                1
            )
        )


        score *= (
            1
            +
            min(
                density / 100,
                2
            )
        )


        traffic_scores[
            f"{name} #{item['number']}"
        ] = score


    # =====================================================
    # 최고 혼잡 공간
    # =====================================================

    if traffic_scores:

        hotspot = max(
            traffic_scores,
            key=traffic_scores.get
        )


        max_score = max(
            traffic_scores.values()
        )


    else:

        hotspot = "없음"

        max_score = 1


    # =====================================================
    # 혼잡도 점수
    # =====================================================

    crowd_score = min(
        100,
        int(
            (
                d["people"]
                /
                max(
                    1,
                    len(layout) * 50
                )
            )
            *
            30
            +
            traffic_scores.get(
                hotspot,
                0
            )
            *
            20
        )
    )


    c1, c2 = st.columns(2)


    with c1:

        st.metric(
            "예상 최대 혼잡도",
            f"{crowd_score}/100"
        )


    with c2:

        st.metric(
            "예상 혼잡 집중 공간",
            hotspot
        )


    # =====================================================
    # 그래프
    # =====================================================

    for name, score in sorted(
        traffic_scores.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        percentage = (
            score
            /
            max_score
            *
            100
        )


        st.write(
            f"**{name}**"
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

    st.divider()

    st.subheader("🚨 혼잡 분석")


    if crowd_score >= 70:

        st.error(
            f"🔴 **{hotspot}** 주변에 "
            "사람이 집중될 가능성이 높습니다."
        )


        st.write(
            "해당 공간 주변 통로를 넓히거나 "
            "대기 공간을 추가하고 프로그램 시간을 분산하는 방법을 고려할 수 있습니다."
        )


    elif crowd_score >= 40:

        st.warning(
            f"🟠 **{hotspot}** 주변에 "
            "참가자가 어느 정도 집중될 것으로 예상됩니다."
        )


        st.write(
            "대기열과 통행로가 겹치지 않도록 관리하는 것이 좋습니다."
        )


    else:

        st.success(
            "🟢 현재 조건에서는 참가자의 이동이 비교적 분산될 것으로 예상됩니다."
        )


    # =====================================================
    # 이동 구조 설명
    # =====================================================

    st.divider()

    st.subheader("🛣️ 사람 이동 경로")


    st.markdown("""
    ### 참가자 이동 방식

    **입구**
    
    ↓
    
    **중앙 통로**
    
    ↓
    
    **각 공간 앞 연결 통로**
    
    ↓
    
    **공간 입구**
    
    ↓
    
    **체험 / 이용**
    
    ↓
    
    **다시 통로**
    
    ↓
    
    **다음 공간**
    
    ↓
    
    **출구**
    
    ---
    
    따라서 참가자가 **부스와 부스 사이를 대각선으로 가로질러 이동하거나
    부스 자체를 관통하는 것이 아니라**, 행사장의 통로를 따라 이동하도록 구성했습니다.
    """)


    # =====================================================
    # 다시 설계
    # =====================================================

    st.divider()


    if st.button(
        "← 입력값 수정하기",
        use_container_width=True
    ):

        st.session_state.page = 1

        st.session_state.design = None

        st.session_state.selected_space = None

        st.rerun()


    st.caption(
        "※ 본 시뮬레이션은 입력된 참가자 수, 행사 목적, 공간 구성 등을 기반으로 한 프로토타입입니다. "
        "실제 행사에서는 현장 도면, 소방·피난 기준, 장애인 접근성 및 실제 보행 데이터를 추가로 검토해야 합니다."
    )
