export function PrivacyPolicyPage() {
  return (
    <div className="min-h-screen bg-background py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold mb-2">プライバシーポリシー</h1>
        <p className="text-sm text-muted-foreground mb-8">最終更新日: 2026年5月12日</p>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">1. はじめに</h2>
          <p className="text-sm text-foreground leading-relaxed">
            麻雀マネージャー（以下「本サービス」）は、LINE Bot および Web アプリケーションとして提供する麻雀対戦成績管理サービスです。
            本サービスをご利用いただくにあたり、収集する情報・利用目的・管理方法についてご説明します。
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">2. 収集する情報</h2>
          <ul className="text-sm text-foreground leading-relaxed space-y-2 list-disc list-inside">
            <li>LINE ユーザー ID・表示名（友達追加時に LINE API から取得）</li>
            <li>LINE グループ ID・グループ名・グループアイコン画像 URL（Bot がグループに参加した際に取得）</li>
            <li>対戦スコアデータ（ユーザーが入力した素点・計算結果・チップ枚数など）</li>
            <li>Google アカウント情報（Web UI ログイン時に取得。メールアドレスは保存しません）</li>
            <li>ランキング画像（生成した画像を Google Cloud Storage に一時保存）</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">3. 情報の利用目的</h2>
          <ul className="text-sm text-foreground leading-relaxed space-y-2 list-disc list-inside">
            <li>麻雀対戦成績の記録・集計・表示</li>
            <li>グループおよびプレイヤーごとのランキング・成績グラフの生成</li>
            <li>LINE Bot からの返信メッセージの送信</li>
            <li>Web UI でのログイン認証</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">4. 第三者への提供</h2>
          <p className="text-sm text-foreground leading-relaxed">
            収集した情報を、法令に基づく場合を除き、第三者に提供・販売・共有することはありません。
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">5. 利用する外部サービス</h2>
          <ul className="text-sm text-foreground leading-relaxed space-y-2 list-disc list-inside">
            <li>LINE Messaging API / LINE Login（LINEヤフー株式会社）</li>
            <li>Google Cloud（Firestore, Cloud Storage, Cloud Run）（Google LLC）</li>
          </ul>
          <p className="text-sm text-muted-foreground mt-2">
            各サービスのプライバシーポリシーについては、各社のサイトをご確認ください。
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">6. データの保管・削除</h2>
          <p className="text-sm text-foreground leading-relaxed">
            収集したデータはサービス提供のために必要な期間保管します。
            データの削除をご希望の場合は、下記のお問い合わせ先までご連絡ください。
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">7. お問い合わせ</h2>
          <p className="text-sm text-foreground leading-relaxed">
            本プライバシーポリシーに関するご質問・データ削除のご依頼は、以下の GitHub リポジトリの Issues よりお問い合わせください。
          </p>
          <a
            href="https://github.com/fezzlk/mahjong-manager-bot/issues"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-primary underline mt-2 inline-block"
          >
            https://github.com/fezzlk/mahjong-manager-bot/issues
          </a>
        </section>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">8. ポリシーの変更</h2>
          <p className="text-sm text-foreground leading-relaxed">
            本ポリシーは必要に応じて更新することがあります。重要な変更がある場合は本ページの「最終更新日」を更新します。
          </p>
        </section>
      </div>
    </div>
  )
}
