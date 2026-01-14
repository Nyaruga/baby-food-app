import streamlit as st
import pandas as pd

# ページの設定
st.set_page_config(page_title="取り分け離乳食レシピ", layout="centered")

st.title("👶 取り分け離乳食チェック")
st.write("判定 ＋ おすすめレシピ ＋ 取り分け術")
st.warning("本サービスは参考情報です。最終判断は医師などに相談の上、保護者様の責任でお願いします。")

@st.cache_data
def load_data():
    # CSVの読み込み
    df = pd.read_csv('food_data.csv')
    # 列名の前後に空白があれば消す
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()

    # 月齢入力
    month = st.number_input("赤ちゃんの月齢（ヶ月）", min_value=1, max_value=24, value=6)
    
    # 食材選択
    selected_foods = st.multiselect(
        "食材を選んでね", 
        options=df['食材名'].tolist()
    )

    if st.button("一括判定する"):
        if not selected_foods:
            st.info("食材を選んでください。")
        else:
            st.divider()
            for food in selected_foods:
                row = df[df['食材名'] == food].iloc[0]
                target_month = row['開始月齢']
                
                # CSVからデータを取り出す
                recipe = row.get('おすすめレシピ名', '設定なし')
                hint = row.get('取り分けヒント', '設定なし')
                howto = row.get('簡単なコツ/作り方', '設定なし')
                link = row.get('詳細リンク', None)

                if month >= target_month:
                    st.success(f"✅ **{food}**：食べられます")
                    # ここが詳細表示のスタートです
                    with st.expander(f"📖 {food} の詳細を見る"):
                        st.write(f"🍳 **レシピ**: {recipe}")
                        st.write(f"💡 **取り分けヒント**: {hint}")
                        st.info(f"👨‍🍳 **簡単なコツ/作り方**: \n\n{howto}")
                        
                        # URLがある場合だけボタンを表示
                        if pd.notna(link) and str(link).startswith('http'):
                            st.link_button("📄 詳しいレシピ（画像・PDF）を開く", link)
                else:
                    st.error(f"❌ **{food}**：{target_month}ヶ月頃から")

except Exception as e:
    st.error(f"エラーが発生しました: {e}")
