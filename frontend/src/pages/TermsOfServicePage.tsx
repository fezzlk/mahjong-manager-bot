export function TermsOfServicePage() {
  return (
    <div className="min-h-screen bg-background py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold mb-2">利用規約</h1>
        <p className="text-sm text-muted-foreground mb-8">最終更新日: 2026年7月25日</p>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">1. はじめに</h2>
          <p className="text-sm text-foreground leading-relaxed">
            この利用規約（以下「本規約」）は、麻雀マネージャー（以下「本サービス」）の LINE Bot および Web
            アプリケーションの利用条件を定めるものです。本サービスをご利用いただく場合、本規約に同意いただいたものとみなします。
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">2. サービス内容</h2>
          <p className="text-sm text-foreground leading-relaxed">
            本サービスは、LINE Bot を通じて麻雀対戦の素点・チップを記録し、Web アプリケーションで対戦履歴・ランキング・成績グラフを閲覧・修正できるサービスです。
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">3. 禁止事項</h2>
          <ul className="text-sm text-foreground leading-relaxed space-y-2 list-disc list-inside">
            <li>虚偽の対戦結果・素点を意図的に入力する行為</li>
            <li>自身が参加していないグループのデータを不正に閲覧・改ざんする行為</li>
            <li>本サービスのサーバー・ネットワークに過度な負荷をかける行為</li>
            <li>他の利用者に迷惑・不利益を与える行為</li>
            <li>法令に違反する行為、その他運営者が不適切と判断する行為</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">4. データの修正・削除</h2>
          <p className="text-sm text-foreground leading-relaxed">
            Web アプリケーション上でグループメンバーは対戦の素点・チップ数の修正、半荘・対戦データの削除を行うことができます。これらの操作は取り消せません。操作内容は運用上の記録として保存されます。
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">5. 免責事項</h2>
          <ul className="text-sm text-foreground leading-relaxed space-y-2 list-disc list-inside">
            <li>本サービスが算出する点数計算結果・ランキング・グラフの正確性を保証するものではありません</li>
            <li>LINE、Google Cloud（Firestore, Cloud Storage, Cloud Run）等の外部サービスの障害・メンテナンスにより本サービスが利用できない場合があります</li>
            <li>利用者の入力誤り・不正な操作によって生じた損害について、運営者は責任を負いません</li>
            <li>運営者は、本サービスの利用によって利用者に生じた損害について、故意または重過失がある場合を除き責任を負いません</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">6. サービスの変更・終了</h2>
          <p className="text-sm text-foreground leading-relaxed">
            運営者は、利用者への事前の通知なく本サービスの内容を変更し、または提供を終了することがあります。
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">7. 準拠法</h2>
          <p className="text-sm text-foreground leading-relaxed">
            本規約の解釈にあたっては、日本法を準拠法とします。
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-lg font-semibold mb-3">8. お問い合わせ</h2>
          <p className="text-sm text-foreground leading-relaxed">
            本規約に関するご質問は、以下の GitHub リポジトリの Issues よりお問い合わせください。
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
          <h2 className="text-lg font-semibold mb-3">9. 規約の変更</h2>
          <p className="text-sm text-foreground leading-relaxed">
            本規約は必要に応じて更新することがあります。重要な変更がある場合は本ページの「最終更新日」を更新します。
          </p>
        </section>

        <p className="text-sm text-muted-foreground">
          関連ページ: <a href="/privacy" className="text-primary underline">プライバシーポリシー</a>
        </p>
      </div>
    </div>
  )
}
