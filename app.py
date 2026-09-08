import streamlit as st
import sqlite3
import hashlib
import math
import random
import html

# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="EVENT:ON",
    page_icon="🎪",
    layout="wide"
)

# =========================================================
# DB - 회원가입 / 로그인
# =========================================================

DB_NAME = "users.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        result = True
    except sqlite3.IntegrityError:
        result = False

    conn.close()
    return result


def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )

    user = cursor.fetchone()
    conn.close()

    return user is not None


init_db()

# =========================================================
# 세션 상태
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = 1

if "design" not in st.session_state:
    st.session_state.design = None

if "selected_space" not in st.session_state:
    st.session_state.selected_space = None

# =========================================================
# 디자인
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 48px;
    font-weight: 800;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 20px;
    color: #666;
    margin-bottom: 30px;
}

.info-card {
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #ddd;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# 공간 정보
# =========================================================
#
# base_area = 기본 공간 면적
# min_area = 최소 면적
# scale = 예상 인원에 따른 확대 정도
#
# booth=True이면 부스처럼 계산
# =========================================================

ELEMENT_INFO = {

    "메인 무대": {
        "icon": "🎤",
        "base_area": 100,
        "min_area": 80,
        "scale": 0.08,
        "booth": False,
        "description": "공연과 주요 프로그램이 진행되는 핵심 공간입니다.",
        "benefit": "관객이 한곳에 집중할 수 있도록 넓은 전면 공간과 충분한 관람 영역을 확보합니다.",
        "traffic": 10
    },

    "체험 부스": {
        "icon": "🎪",
        "base_area": 9,
        "min_area": 9,
        "scale": 0.0,
        "booth": True,
        "description": "참가자가 직접 체험하는 소규모 프로그램 공간입니다.",
        "benefit": "작은 면적으로도 여러 프로그램을 운영할 수 있어 행사 콘텐츠를 다양하게 구성할 수 있습니다.",
        "traffic": 7
    },

    "대형 체험 부스": {
        "icon": "🏗️",
        "base_area": 16,
        "min_area": 16,
        "scale": 0.0,
        "booth": True,
        "description": "여러 명이 동시에 참여하는 대형 체험 공간입니다.",
        "benefit": "동시에 많은 참가자를 수용할 수 있어 인기 체험 프로그램의 대기열을 줄이는 데 유리합니다.",
        "traffic": 9
    },

    "푸드존": {
        "icon": "🍴",
        "base_area": 40,
        "min_area": 35,
        "scale": 0.03,
        "booth": False,
        "description": "음식과 음료를 판매하고 식사할 수 있는 공간입니다.",
        "benefit": "장시간 행사에서 체류 시간을 늘리고 휴식과 식사를 동시에 해결할 수 있습니다.",
        "traffic": 8
    },

    "포토존": {
        "icon": "📸",
        "base_area": 15,
        "min_area": 12,
        "scale": 0.0,
        "booth": False,
        "description": "사진 촬영과 행사 홍보를 위한 공간입니다.",
        "benefit": "행사의 시각적 특징을 만들고 참가자의 자발적인 SNS 공유를 유도할 수 있습니다.",
        "traffic": 6
    },

    "휴식 공간": {
        "icon": "🛋️",
        "base_area": 25,
        "min_area": 20,
        "scale": 0.02,
        "booth": False,
        "description": "참가자가 앉아서 쉬거나 대기할 수 있는 공간입니다.",
        "benefit": "장시간 행사에서 피로를 줄이고 고령층이나 어린이 이용자의 편의성을 높입니다.",
        "traffic": 5
    },

    "화장실": {
        "icon": "🚻",
        "base_area": 20,
        "min_area": 15,
        "scale": 0.015,
        "booth": False,
        "description": "참가자를 위한 화장실 및 편의시설입니다.",
        "benefit": "행사장 곳곳에서 접근하기 쉽도록 주요 동선과 가까운 위치에 배치하는 것이 좋습니다.",
        "traffic": 7
    },

    "안내소": {
        "icon": "ℹ️",
        "base_area": 12,
        "min_area": 10,
        "scale": 0.0,
        "booth": False,
        "description": "행사 정보와 위치를 안내하는 공간입니다.",
        "benefit": "입구 근처에 배치하면 참가자의 초기 이동 혼란을 줄일 수 있습니다.",
        "traffic": 8
    },

    "응급의료소": {
        "icon": "🚑",
        "base_area": 18,
        "min_area": 15,
        "scale": 0.0,
        "booth": False,
        "description": "응급 상황 발생 시 의료 대응을 위한 공간입니다.",
        "benefit": "출입구와 주요 행사장 모두에서 빠르게 접근할 수 있도록 배치하는 것이 중요합니다.",
        "traffic": 3
    },

    "대기 공간": {
        "icon": "⏳",
        "base_area": 30,
        "min_area": 20,
        "scale": 0.03,
        "booth": False,
        "description": "입장이나 인기 프로그램 이용 전에 대기하는 공간입니다.",
        "benefit": "대기열을 통로에서 분리하여 전체 행사장의 흐름을 방해하지 않도록 할 수 있습니다.",
        "traffic": 7
    },

    "굿즈 판매": {
        "icon": "🛍️",
        "base_area": 18,
        "min_area": 12,
        "scale": 0.01,
        "booth": True,
        "description": "행사 관련 상품을 판매하는 공간입니다.",
        "benefit": "출구 또는 주요 동선 주변에 배치하면 행사 종료 후 자연스럽게 방문을 유도할 수 있습니다.",
        "traffic": 7
    },

    "장애인 편의시설": {
        "icon": "♿",
        "base_area": 20,
        "min_area": 15,
        "scale": 0.01,
        "booth": False,
        "description": "휠체어 이용자와 이동이 어려운 참가자를 위한 편의 공간입니다.",
        "benefit": "주요 공간과 연결되는 접근 가능한 동선을 확보하는 데 도움이 됩니다.",
        "traffic": 3
    }
}

# =========================================================
# 행사 유형별 목적
# =========================================================

PURPOSES = {
    "축제": [
        "많은 사람이 다양한 프로그램을 즐기는 행사",
        "공연 중심의 축제",
        "체험 부스 중심의 축제",
        "먹거리와 문화 중심의 축제"
    ],

    "학교 행사": [
        "학생 참여 중심 행사",
        "동아리 홍보 행사",
        "학교 축제",
        "진로·교육 행사"
    ],

    "박람회": [
        "기업·기관 홍보",
        "교육·진로 박람회",
        "과학·기술 박람회",
        "체험형 박람회"
    ],

    "공연": [
        "음악 공연",
        "학교 공연",
        "문화 공연",
        "대규모 콘서트"
    ],

    "체험 행사": [
        "과학 체험",
        "문화 체험",
        "교육 체험",
        "가족 체험"
    ],

    "지역 행사": [
        "지역 주민 축제",
        "지역 특산물 행사",
        "문화 행사",
        "관광 행사"
    ],

    "전시회": [
        "미술 전시",
        "과학 전시",
        "학교 작품 전시",
        "기업 전시"
    ],

    "스포츠 행사": [
        "학교 체육 행사",
        "지역 스포츠 행사",
        "대회",
        "체험형 스포츠 행사"
    ]
}

# =========================================================
# 행사 유형별 추천 공간
# =========================================================

RECOMMENDED = {

    "축제": [
        "메인 무대",
        "체험 부스",
        "대형 체험 부스",
        "푸드존",
        "포토존",
        "휴식 공간",
        "화장실",
        "안내소",
        "응급의료소"
    ],

    "학교 행사": [
        "메인 무대",
        "체험 부스",
        "휴식 공간",
        "포토존",
        "화장실",
        "안내소",
        "응급의료소"
    ],

    "박람회": [
        "체험 부스",
        "대형 체험 부스",
        "안내소",
        "휴식 공간",
        "화장실",
        "응급의료소"
    ],

    "공연": [
        "메인 무대",
        "대기 공간",
        "굿즈 판매",
        "휴식 공간",
        "화장실",
        "안내소",
        "응급의료소"
    ],

    "체험 행사": [
        "체험 부스",
        "대형 체험 부스",
        "대기 공간",
        "휴식 공간",
        "화장실",
        "안내소",
        "응급의료소"
    ],

    "지역 행사": [
        "메인 무대",
        "체험 부스",
        "푸드존",
        "포토존",
        "휴식 공간",
        "화장실",
        "안내소"
    ],

    "전시회": [
        "체험 부스",
        "대형 체험 부스",
        "안내소",
        "휴식 공간",
        "화장실"
    ],

    "스포츠 행사": [
        "메인 무대",
        "대기 공간",
        "휴식 공간",
        "화장실",
        "응급의료소",
        "안내소"
    ]
}

# =========================================================
# 공간 실제 면적 계산
# =========================================================

def calculate_space_area(name, people):
    info = ELEMENT_INFO.get(name)

    if not info:
        return 12

    area = info["base_area"]

    if info["scale"] > 0:
        area += people * info["scale"]

    return max(info["min_area"], round(area))


# =========================================================
# 전체 행사장 면적
# =========================================================

def calculate_venue_area(people, location_type):

    if location_type == "실내":
        per_person = 1.8
    else:
        per_person = 2.5

    return max(300, math.ceil(people * per_person))


# =========================================================
# 혼잡도
# =========================================================

def calculate_crowding(people, duration):

    density = people / max(duration, 1)

    if density < 100:
        return "낮음"

    elif density < 250:
        return "보통"

    elif density < 500:
        return "높음"

    return "매우 높음"


# =========================================================
# 실제 공간 크기 계산
# =========================================================

def rectangle_size(area):

    # 행사장 안에서 보이기 좋은 가로:세로 비율
    aspect_ratio = 1.5

    width = math.sqrt(area * aspect_ratio)
    height = area / width

    return width, height


# =========================================================
# 실제 행사장 Layout 생성
#
# 핵심:
# 공간 크기가 서로 다름
# 공간 사이에는 통로가 존재
# 최대 12개 제한 없음
# =========================================================

def create_realistic_layout(selected_spaces, venue_area):

    # -----------------------------------------------------
    # 행사장 실제 크기
    # -----------------------------------------------------

    venue_width = math.sqrt(venue_area * 1.5)
    venue_height = venue_area / venue_width

    # 통로 폭
    corridor_width = 4.0

    # 외곽 여백
    margin = 3.0

    usable_width = venue_width - margin * 2

    # -----------------------------------------------------
    # 공간 목록 만들기
    # -----------------------------------------------------

    spaces = []

    for name, count in selected_spaces.items():

        for i in range(count):

            area = calculate_space_area(
                name,
                st.session_state.get("people", 500)
            )

            width, height = rectangle_size(area)

            spaces.append({
                "name": name,
                "number": i + 1,
                "area": area,
                "width": width,
                "height": height
            })

    # 큰 공간부터 배치
    spaces.sort(
        key=lambda x: x["area"],
        reverse=True
    )

    # -----------------------------------------------------
    # 행 기반 배치
    #
    # 각 행:
    #
    # ┌ 부스 ┐ ┌ 부스 ┐
    # ──────────────── 통로
    # └ 부스 ┘ └ 부스 ┘
    #
    # 이런 식으로 공간과 통로를 분리
    # -----------------------------------------------------

    rows = []

    current_row = []
    current_width = 0
    current_height = 0

    for space in spaces:

        required_width = space["width"] + corridor_width

        if (
            current_row
            and current_width + required_width > usable_width
        ):

            rows.append({
                "spaces": current_row,
                "height": current_height
            })

            current_row = []
            current_width = 0
            current_height = 0

        current_row.append(space)

        current_width += required_width

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
    # 실제 좌표 계산
    # -----------------------------------------------------

    layout = []

    y = margin + 10

    for row_index, row in enumerate(rows):

        row_height = row["height"]

        x = margin

        for space in row["spaces"]:

            w = space["width"]
            h = space["height"]

            # 통로와 접하도록 공간 배치
            layout.append({
                "name": space["name"],
                "number": space["number"],
                "area": space["area"],
                "x": x,
                "y": y,
                "width": w,
                "height": h,
                "row": row_index
            })

            x += w + corridor_width

        # 다음 행
        y += row_height + corridor_width

    # -----------------------------------------------------
    # 행사장이 부족하면 전체를 비율 조정
    # -----------------------------------------------------

    used_height = y + margin

    if used_height > venue_height:

        scale = (
            (venue_height - margin * 2)
            / max(used_height - margin, 1)
        )

        for item in layout:

            item["x"] *= scale
            item["y"] *= scale
            item["width"] *= scale
            item["height"] *= scale

    return layout, venue_width, venue_height


# =========================================================
# 통로 계산
#
# 모든 이동은 이 통로를 통해서만 이루어짐
# =========================================================

def build_corridors(layout, venue_width, venue_height):

    corridors = []

    # 중앙 세로 메인 통로
    center_x = venue_width / 2

    corridors.append({
        "type": "vertical",
        "x1": center_x,
        "y1": 0,
        "x2": center_x,
        "y2": venue_height
    })

    # 각 공간의 중심 높이에 맞춰 가로 통로 생성
    y_values = []

    for item in layout:

        center_y = (
            item["y"]
            + item["height"] / 2
        )

        if all(
            abs(center_y - existing) > 5
            for existing in y_values
        ):
            y_values.append(center_y)

    for y in y_values:

        corridors.append({
            "type": "horizontal",
            "x1": 0,
            "y1": y,
            "x2": venue_width,
            "y2": y
        })

    return corridors


# =========================================================
# 가장 가까운 통로점
# =========================================================

def nearest_corridor_point(
    space,
    venue_width,
    venue_height
):

    center_x = (
        space["x"]
        + space["width"] / 2
    )

    center_y = (
        space["y"]
        + space["height"] / 2
    )

    main_corridor_x = venue_width / 2

    # 공간의 좌우 중 중앙 통로에 가까운 쪽 선택
    if center_x < main_corridor_x:

        target_x = space["x"] + space["width"]

    else:

        target_x = space["x"]

    target_y = center_y

    return target_x, target_y


# =========================================================
# 통로 기반 이동 경로
#
# 중요:
# 공간 내부를 통과하지 않고
# 통로 → 통로 → 목적지 입구로 이동
# =========================================================

def make_path_to_space(
    space,
    venue_width,
    venue_height
):

    center_x = venue_width / 2

    target_x, target_y = nearest_corridor_point(
        space,
        venue_width,
        venue_height
    )

    entrance_x = center_x
    entrance_y = venue_height

    # 입구 → 중앙 세로 통로 → 해당 공간 앞 통로
    path = [
        (entrance_x, entrance_y),
        (center_x, target_y),
        (target_x, target_y)
    ]

    return path


# =========================================================
# SVG 좌표 변환
# =========================================================

def sx(x, venue_width):
    return x / venue_width * 120


def sy(y, venue_height):
    return y / venue_height * 90


def sw(width, venue_width):
    return width / venue_width * 120


def sh(height, venue_height):
    return height / venue_height * 90


# =========================================================
# SVG 행사장 생성
# =========================================================

def create_floorplan_svg(
    layout,
    venue_width,
    venue_height,
    simulation=False,
    people_count=30
):

    svg_width = 120
    svg_height = 90

    parts = []

    parts.append(
        f"""
        <svg
            viewBox="0 0 {svg_width} {svg_height}"
            width="100%"
            xmlns="http://www.w3.org/2000/svg"
        >
        """
    )

    # -----------------------------------------------------
    # 행사장 배경
    # -----------------------------------------------------

    parts.append("""
        <rect
            x="1"
            y="1"
            width="118"
            height="88"
            rx="4"
            fill="#fafafa"
            stroke="#333"
            stroke-width="0.8"
        />
    """)

    # -----------------------------------------------------
    # 통로
    # -----------------------------------------------------

    center_x = sx(
        venue_width / 2,
        venue_width
    )

    # 중앙 세로 통로
    parts.append(
        f"""
        <rect
            x="{center_x - 2.2}"
            y="5"
            width="4.4"
            height="77"
            rx="1"
            fill="#eeeeee"
        />
        """
    )

    # -----------------------------------------------------
    # 공간
    # -----------------------------------------------------

    for index, item in enumerate(layout):

        x = sx(item["x"], venue_width)
        y = sy(item["y"], venue_height)

        w = sw(item["width"], venue_width)
        h = sh(item["height"], venue_height)

        name = html.escape(item["name"])

        label = (
            f"{item['area']}㎡"
        )

        # 큰 공간일수록 조금 더 진하게 표시
        if item["area"] >= 80:
            fill = "#dfe9ff"

        elif item["area"] >= 30:
            fill = "#e8f4e8"

        else:
            fill = "#fff3d6"

        parts.append(
            f"""
            <rect
                x="{x}"
                y="{y}"
                width="{w}"
                height="{h}"
                rx="1.5"
                fill="{fill}"
                stroke="#444"
                stroke-width="0.45"
            />
            """
        )

        # 이름
        font_size = min(
            3.0,
            max(1.4, w / 8)
        )

        parts.append(
            f"""
            <text
                x="{x + w / 2}"
                y="{y + h / 2 - 0.8}"
                text-anchor="middle"
                font-size="{font_size}"
                font-weight="bold"
                fill="#222"
            >
                {name}
            </text>
            """
        )

        parts.append(
            f"""
            <text
                x="{x + w / 2}"
                y="{y + h / 2 + 2.3}"
                text-anchor="middle"
                font-size="1.6"
                fill="#555"
            >
                {label}
            </text>
            """
        )

    # -----------------------------------------------------
    # 입구
    # -----------------------------------------------------

    parts.append("""
        <rect
            x="53"
            y="85"
            width="14"
            height="4"
            rx="1"
            fill="#d9ead3"
            stroke="#333"
        />

        <text
            x="60"
            y="87.7"
            text-anchor="middle"
            font-size="2"
            font-weight="bold"
        >
            🚪 입구
        </text>
    """)

    # -----------------------------------------------------
    # 출구
    # -----------------------------------------------------

    parts.append("""
        <rect
            x="53"
            y="1"
            width="14"
            height="4"
            rx="1"
            fill="#f4cccc"
            stroke="#333"
        />

        <text
            x="60"
            y="3.7"
            text-anchor="middle"
            font-size="2"
            font-weight="bold"
        >
            🚪 출구
        </text>
    """)

    # =====================================================
    # 시뮬레이션
    # =====================================================

    if simulation and layout:

        # 참가자 수는 화면에 너무 많지 않게 표시
        visual_people = min(
            80,
            max(20, people_count // 10)
        )

        random.seed(42)

        for person_index in range(visual_people):

            target = random.choice(layout)

            path = make_path_to_space(
                target,
                venue_width,
                venue_height
            )

            # SVG 좌표로 변환
            points = []

            for px, py in path:

                points.append(
                    f"{sx(px, venue_width):.2f},"
                    f"{sy(py, venue_height):.2f}"
                )

            points_text = " ".join(points)

            delay = (
                person_index * 0.13
            )

            duration = (
                5.0
                + random.random() * 3
            )

            parts.append(
                f"""
                <circle
                    r="0.65"
                    fill="#333"
                    opacity="0.75"
                >
                    <animateMotion
                        dur="{duration:.2f}s"
                        begin="{delay:.2f}s"
                        repeatCount="indefinite"
                        path="M {points_text.replace(',', ' ')}"
                    />
                </circle>
                """
            )

    parts.append("</svg>")

    return "".join(parts)


# =========================================================
# 혼잡 분석
# =========================================================

def calculate_space_traffic(
    layout,
    people,
    duration
):

    scores = []

    for item in layout:

        info = ELEMENT_INFO.get(
            item["name"],
            {}
        )

        base = info.get(
            "traffic",
            5
        )

        # 면적이 작고 방문자가 많이 몰리는 경우
        density_factor = (
            people / max(item["area"], 1)
        )

        score = base * (
            1 + min(
                density_factor / 100,
                2
            )
        )

        scores.append({
            "name": item["name"],
            "number": item["number"],
            "area": item["area"],
            "score": score
        })

    return scores


# =========================================================
# 로그인 화면
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="main-title">🎪 EVENT:ON</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        '사용자의 니즈를 분석해 최적의 행사장을 설계합니다.'
        '</div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(
        ["🔐 로그인", "📝 회원가입"]
    )

    with tab1:

        st.subheader("로그인")

        username = st.text_input(
            "아이디",
            key="login_username"
        )

        password = st.text_input(
            "비밀번호",
            type="password",
            key="login_password"
        )

        if st.button(
            "로그인",
            use_container_width=True
        ):

            if not username or not password:

                st.warning(
                    "아이디와 비밀번호를 입력해주세요."
                )

            elif login_user(
                username,
                password
            ):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    "아이디 또는 비밀번호가 올바르지 않습니다."
                )

    with tab2:

        st.subheader("회원가입")

        new_username = st.text_input(
            "새 아이디",
            key="register_username"
        )

        new_password = st.text_input(
            "새 비밀번호",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "비밀번호 확인",
            type="password",
            key="register_password_confirm"
        )

        if st.button(
            "회원가입",
            use_container_width=True
        ):

            if not new_username or not new_password:

                st.warning(
                    "아이디와 비밀번호를 입력해주세요."
                )

            elif new_password != confirm_password:

                st.error(
                    "비밀번호가 일치하지 않습니다."
                )

            elif len(new_password) < 4:

                st.warning(
                    "비밀번호는 4자 이상으로 설정해주세요."
                )

            elif register_user(
                new_username,
                new_password
            ):

                st.success(
                    "회원가입 완료! 로그인해주세요."
                )

            else:

                st.error(
                    "이미 존재하는 아이디입니다."
                )

    st.stop()


# =========================================================
# 로그인 후
# =========================================================

st.sidebar.success(
    f"현재 로그인: {st.session_state.username}"
)

if st.sidebar.button("로그아웃"):

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()


st.markdown(
    '<div class="main-title">🎪 EVENT:ON</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    '사용자의 니즈를 분석하여 실제 행사장 구조와 사람의 이동을 설계합니다.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# PAGE 1
# =========================================================

if st.session_state.page == 1:

    st.header("🎯 1단계 — 행사 정보 입력")

    col1, col2 = st.columns(2)

    with col1:

        event_type = st.selectbox(
            "행사장의 유형",
            list(PURPOSES.keys())
        )

        purpose = st.selectbox(
            "행사의 목적",
            PURPOSES[event_type]
        )

        people = st.number_input(
            "예상 방문객 수",
            min_value=10,
            max_value=100000,
            value=500,
            step=10
        )

        duration = st.number_input(
            "진행 시간",
            min_value=1,
            max_value=24,
            value=4
        )

    with col2:

        age_group = st.selectbox(
            "예상 연령대",
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
            "예상 입장료 (원)",
            min_value=0,
            max_value=1000000,
            value=0,
            step=1000
        )

        location_type = st.radio(
            "행사 장소",
            ["실내", "실외"],
            horizontal=True
        )

    st.session_state.people = people

    # =====================================================
    # 공간 선택
    # =====================================================

    st.divider()

    st.header("🏗️ 2단계 — 필요한 공간 선택")

    st.info(
        "각 공간은 실제 필요한 면적을 다르게 계산합니다. "
        "원하지 않는 공간은 0개로 설정할 수 있습니다."
    )

    selected_spaces = {}

    recommended = RECOMMENDED[event_type]

    for i in range(0, len(recommended), 3):

        cols = st.columns(3)

        for j, name in enumerate(
            recommended[i:i + 3]
        ):

            with cols[j]:

                info = ELEMENT_INFO[name]

                st.markdown(
                    f"### {info['icon']} {name}"
                )

                area_preview = calculate_space_area(
                    name,
                    people
                )

                st.caption(
                    f"기본 예상 면적: 약 {area_preview}㎡"
                )

                count = st.number_input(
                    f"{name} 개수",
                    min_value=0,
                    max_value=100,
                    value=1,
                    step=1,
                    key=f"count_{event_type}_{name}"
                )

                selected_spaces[name] = count

    # =====================================================
    # 추가 공간
    # =====================================================

    st.divider()

    st.subheader("➕ 직접 추가 공간")

    custom_name = st.text_input(
        "추가하고 싶은 공간 이름"
    )

    custom_count = 0

    if custom_name.strip():

        custom_count = st.number_input(
            f"{custom_name} 개수",
            min_value=0,
            max_value=100,
            value=1,
            step=1
        )

        if custom_name not in ELEMENT_INFO:

            ELEMENT_INFO[custom_name] = {
                "icon": "📦",
                "base_area": 12,
                "min_area": 8,
                "scale": 0.0,
                "booth": True,
                "description": "사용자가 직접 추가한 행사 공간입니다.",
                "benefit": "사용자가 원하는 프로그램에 맞게 자유롭게 구성할 수 있습니다.",
                "traffic": 5
            }

        selected_spaces[custom_name] = custom_count

    # =====================================================
    # 설계 버튼
    # =====================================================

    st.divider()

    if st.button(
        "🚀 실제 행사장 설계 시작",
        use_container_width=True
    ):

        # 0개 공간 제거
        final_spaces = {
            name: count
            for name, count
            in selected_spaces.items()
            if count > 0
        }

        if not final_spaces:

            st.error(
                "최소 하나 이상의 공간을 1개 이상 선택해주세요."
            )

        else:

            venue_area = calculate_venue_area(
                people,
                location_type
            )

            layout, venue_width, venue_height = (
                create_realistic_layout(
                    final_spaces,
                    venue_area
                )
            )

            traffic = calculate_space_traffic(
                layout,
                people,
                duration
            )

            st.session_state.design = {
                "event_type": event_type,
                "purpose": purpose,
                "people": people,
                "duration": duration,
                "age_group": age_group,
                "atmosphere": atmosphere,
                "entrance_fee": entrance_fee,
                "location_type": location_type,
                "spaces": final_spaces,
                "layout": layout,
                "venue_area": venue_area,
                "venue_width": venue_width,
                "venue_height": venue_height,
                "traffic": traffic
            }

            st.session_state.page = 2

            st.rerun()


# =========================================================
# PAGE 2
# =========================================================

else:

    design = st.session_state.design

    event_type = design["event_type"]
    purpose = design["purpose"]
    people = design["people"]
    duration = design["duration"]
    age_group = design["age_group"]
    atmosphere = design["atmosphere"]
    location_type = design["location_type"]

    layout = design["layout"]
    venue_width = design["venue_width"]
    venue_height = design["venue_height"]

    st.header("🗺️ 3단계 — 자동 생성된 실제 행사장 배치도")

    st.success(
        f"'{event_type}' / '{purpose}' 조건을 반영하여 "
        f"총 {len(layout)}개의 공간을 배치했습니다."
    )

    # =====================================================
    # 핵심 정보
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "예상 방문객",
            f"{people:,}명"
        )

    with c2:
        st.metric(
            "행사장 면적",
            f"{design['venue_area']:,}㎡"
        )

    with c3:
        st.metric(
            "배치 공간",
            f"{len(layout)}개"
        )

    with c4:
        st.metric(
            "예상 혼잡도",
            calculate_crowding(
                people,
                duration
            )
        )

    # =====================================================
    # 실제 배치도
    # =====================================================

    svg = create_floorplan_svg(
        layout,
        venue_width,
        venue_height,
        simulation=False
    )

    st.components.v1.html(
        svg,
        height=700,
        scrolling=False
    )

    st.caption(
        "※ 각 공간의 크기는 실제 예상 필요 면적을 기반으로 서로 다르게 계산되었습니다."
    )

    # =====================================================
    # 공간 상세 정보
    # =====================================================

    st.divider()

    st.subheader("🔎 공간 상세 정보")

    names = []

    for item in layout:

        label = (
            f"{ELEMENT_INFO[item['name']]['icon']} "
            f"{item['name']} #{item['number']} "
            f"({item['area']}㎡)"
        )

        names.append(label)

    selected_label = st.selectbox(
        "확인할 공간을 선택하세요",
        names
    )

    selected_index = names.index(
        selected_label
    )

    selected_item = layout[selected_index]

    info = ELEMENT_INFO[
        selected_item["name"]
    ]

    st.markdown(
        f"""
        ### {info['icon']} {selected_item['name']} #{selected_item['number']}

        **실제 배정 면적:** {selected_item['area']}㎡

        **공간 설명:**  
        {info['description']}

        **이 공간의 장점:**  
        {info['benefit']}
        """
    )

    # =====================================================
    # 공간별 크기 표
    # =====================================================

    st.divider()

    st.subheader("📐 공간별 실제 크기")

    for item in layout:

        st.write(
            f"**{item['name']} #{item['number']}** — "
            f"{item['area']}㎡ "
            f"({item['width']:.1f}m × {item['height']:.1f}m)"
        )

    # =====================================================
    # 시뮬레이션
    # =====================================================

    st.divider()

    st.header("🚶 4단계 — 동일 배치도 기반 이동 시뮬레이션")

    st.info(
        "아래 시뮬레이션은 위에서 생성된 것과 **동일한 배치도와 좌표**를 사용합니다. "
        "사람은 공간 내부를 가로질러 이동하지 않고 행사장 통로를 따라 이동하도록 설정했습니다."
    )

    simulation_svg = create_floorplan_svg(
        layout,
        venue_width,
        venue_height,
        simulation=True,
        people_count=people
    )

    st.components.v1.html(
        simulation_svg,
        height=700,
        scrolling=False
    )

    # =====================================================
    # 혼잡 분석
    # =====================================================

    st.subheader("📊 공간별 예상 혼잡")

    traffic = design["traffic"]

    sorted_traffic = sorted(
        traffic,
        key=lambda x: x["score"],
        reverse=True
    )

    max_score = (
        sorted_traffic[0]["score"]
        if sorted_traffic
        else 1
    )

    for item in sorted_traffic:

        percentage = (
            item["score"]
            / max_score
            * 100
        )

        st.write(
            f"**{item['name']} #{item['number']}** "
            f"— {item['area']}㎡"
        )

        st.progress(
            min(
                1.0,
                percentage / 100
            )
        )

    if sorted_traffic:

        hotspot = sorted_traffic[0]

        st.warning(
            f"🔥 예상 혼잡 집중 공간: "
            f"{hotspot['name']} #{hotspot['number']} "
            f"({hotspot['area']}㎡)"
        )

        st.write(
            "이 공간으로 이동하는 참가자가 많을 것으로 예상되므로 "
            "주변 통로의 폭을 넓히거나 프로그램 시간을 분산하는 방법을 고려할 수 있습니다."
        )

    # =====================================================
    # 동선 설명
    # =====================================================

    st.divider()

    st.subheader("🛣️ 이동 동선 설계 원리")

    st.markdown("""
    **입구**
    ↓  
    **중앙 메인 통로**
    ↓  
    **각 공간 앞의 연결 통로**
    ↓  
    **목적 공간**
    ↓  
    **다시 통로로 이동**
    ↓  
    **출구**

    따라서 참가자가 부스나 시설을 직접 관통해서 이동하는 것이 아니라,
    **행사장에 생성된 통로 네트워크를 따라 이동하도록 설계했습니다.**
    """)

    # =====================================================
    # 다시 설계
    # =====================================================

    st.divider()

    if st.button(
        "← 조건을 수정해서 다시 설계하기",
        use_container_width=True
    ):

        st.session_state.page = 1
        st.session_state.design = None

        st.rerun()

    st.caption(
        "※ 본 시뮬레이션은 기획 단계의 프로토타입입니다. "
        "실제 행사에서는 현장 도면, 소방·피난 기준, 장애인 접근성, "
        "시설물 규격 및 실제 보행 데이터를 추가로 검토해야 합니다."
    )
