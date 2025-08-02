<h1>履修のミカタ</h1>

<p><strong>履修のミカタ</strong>は、学生が授業情報を検索・登録・レビューできるWebアプリです。Google Sheetsと連携し、履修情報の一元管理と他ユーザーとの交流を実現します。</p>

<h2>主な機能</h2>
<ul>
  <li>授業検索（授業名、教員名、学期、曜日、キーワード）</li>
  <li>授業レビュー（評価・コメントを投稿／削除、他ユーザーのレビューを検索）</li>
  <li>時間割表示（登録授業を学期ごとに表示、ワンタッチ履修登録／キャンセル）</li>
  <li>先生検索（専門分野・所属など）</li>
  <li>ユーザー認証（学生番号との連携）</li>
</ul>

<h2>セットアップ方法</h2>

<h3>1. 必要パッケージのインストール</h3>
<p>このアプリの動作には、以下のパッケージが必要です。ターミナルで以下のコマンドを実行してください。</p>
<pre><code>pip install -r requirements.txt</code></pre>
<p><code>requirements.txt</code> はこのプロジェクトに含まれています。</p>

<h3>2. Google Sheets API 連携</h3>
<ul>
  <li><strong>開発者から渡された <code>auth.json</code> ファイル</strong> を、このフォルダに保存してください。</li>
</ul>

<h3>3. アプリ起動</h3>
<pre><code>streamlit run main.py</code></pre>

<h2>データ構成（Google Sheets）</h2>
<table>
  <thead>
    <tr>
      <th>シート名</th>
      <th>内容</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>student</td><td>学籍番号・名前・所属</td></tr>
    <tr><td>lecture</td><td>授業ID・授業名・教員・学期・曜日</td></tr>
    <tr><td>review</td><td>授業ID・評価・コメント・投稿者・時刻</td></tr>
    <tr><td>teacher</td><td>教員名・専門分野・所属など</td></tr>
  </tbody>
</table>

<h2>ページ構成</h2>
<ul>
  <li><code>main.py</code>：全体のページ制御と起動ポイント</li>
  <li><code>student_page.py</code>：🏠 トップページ（学生情報の登録・ログイン）</li>
  <li><code>edit_profile.py</code>：🗓️ プロフィール編集（時間割の表示・履修管理）</li>
  <li><code>lecture_page.py</code>：📖 授業検索・履修登録ページ</li>
  <li><code>review_page.py</code>：🗣️ 授業レビュー投稿・検索ページ</li>
  <li><code>timetable_page.py</code>：📅 全授業の時間割表示（学期別）</li>
  <li><code>teacher_page.py</code>：👨‍🏫 教員検索ページ</li>
  <li><code>auth.py</code>：🔐 Google Sheets認証（サービスアカウント）</li>
</ul>

<h2>📬 お問い合わせ</h2>
<p>ご質問は<code>oba.kohei.262@s.kyushu-u.ac.jp</code> までお願いします。</p>

</body>
</html>
