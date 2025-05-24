// メインJavaScriptファイル

// グローバル変数
let chart;
let activeYears = {};

// DOMが読み込まれたら実行
document.addEventListener('DOMContentLoaded', function() {
    // データが既にロードされているか確認（plot_data.jsから）
    if (typeof plotData !== 'undefined') {
        initializeChart();
    } else {
        // データがない場合はエラーメッセージを表示
        document.getElementById('loading').innerHTML = '<p>データの読み込みに失敗しました。</p>';
    }
});

// チャートの初期化
function initializeChart() {
    try {
        // Plotlyデータを使用
        const figure = plotData;
        
        // チャートを描画
        Plotly.newPlot('chart', figure.data, figure.layout, {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['select2d', 'lasso2d', 'autoScale2d']
        });
        
        // ローディング表示を非表示
        document.getElementById('loading').style.display = 'none';
        
        // 年度トグルボタンを生成
        createYearToggleButtons(figure.data);
        
        // 最終更新日時を設定
        updateLastUpdatedTime();
        
        // グローバル変数に保存
        chart = figure;
    } catch (error) {
        console.error('チャートの初期化エラー:', error);
        document.getElementById('loading').innerHTML = '<p>チャートの初期化に失敗しました。</p>';
    }
}

// 年度トグルボタンを生成
function createYearToggleButtons(data) {
    const toggleContainer = document.getElementById('year-toggles');
    const years = new Set();
    
    // 利用可能な年度を収集
    data.forEach(trace => {
        const year = trace.name.replace('年', '');
        years.add(year);
        activeYears[year] = true; // 初期状態ではすべての年度を表示
    });
    
    // 年度を昇順にソート
    const sortedYears = Array.from(years).sort();
    
    // 各年度のボタンを作成
    sortedYears.forEach(year => {
        const button = document.createElement('button');
        button.textContent = `${year}年`;
        button.className = 'year-button';
        button.dataset.year = year;
        
        // クリックイベントを追加
        button.addEventListener('click', function() {
            toggleYearVisibility(year, button);
        });
        
        toggleContainer.appendChild(button);
    });
}

// 年度の表示/非表示を切り替え
function toggleYearVisibility(year, button) {
    // 状態を反転
    activeYears[year] = !activeYears[year];
    
    // ボタンのスタイルを更新
    if (activeYears[year]) {
        button.classList.remove('inactive');
    } else {
        button.classList.add('inactive');
    }
    
    // チャートの表示を更新
    updateChartVisibility();
}

// チャートの表示を更新
function updateChartVisibility() {
    const chartDiv = document.getElementById('chart');
    const data = chart.data;
    
    // 各トレースの表示/非表示を設定
    const updatedVisibility = data.map(trace => {
        const year = trace.name.replace('年', '');
        return activeYears[year];
    });
    
    // チャートを更新
    Plotly.restyle(chartDiv, {
        visible: updatedVisibility
    });
}

// 最終更新日時を設定
function updateLastUpdatedTime() {
    const now = new Date();
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit',
        timeZone: 'Asia/Tokyo'
    };
    
    const formattedDate = now.toLocaleDateString('ja-JP', options);
    document.getElementById('last-updated').textContent = formattedDate;
}

// ウィンドウサイズ変更時にチャートをリサイズ
window.addEventListener('resize', function() {
    Plotly.Plots.resize(document.getElementById('chart'));
});
