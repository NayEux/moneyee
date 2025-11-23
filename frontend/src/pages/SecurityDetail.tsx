import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../api'
import { Card, Row, Col, Button, Table } from 'antd'
import ReactECharts from 'echarts-for-react'

const SecurityDetail: React.FC = () => {
  const { symbol } = useParams()
  const [market] = useState('US')
  const [context, setContext] = useState<any>(null)

  const load = () => {
    api.get(`/api/ai_context/security/${symbol}`, { params: { market, price_days: 60, news_limit: 5, research_limit: 3 } }).then(res => setContext(res.data))
  }

  useEffect(() => { load() }, [symbol])

  const priceOption = {
    xAxis: { type: 'category', data: context?.price_history?.map((p: any) => p.date) ?? [] },
    yAxis: { type: 'value' },
    series: [{ data: context?.price_history?.map((p: any) => p.close) ?? [], type: 'line' }]
  }

  const triggerAnalysis = async () => {
    await api.post('/api/ai_analysis', { security_id: context.security.id, analysis_type: 'single_stock', result_json: { rating: 'buy', rationale: 'Mock rationale' } })
    load()
  }

  return (
    <div>
      <Row gutter={16}>
        <Col span={12}><Card title="基本信息">{context?.security?.name} ({context?.security?.symbol})</Card></Col>
        <Col span={12}><Card title="最新报价">{context?.latest_quote?.price}</Card></Col>
      </Row>
      <Card title="价格走势" style={{ marginTop: 16 }}>
        <ReactECharts style={{ height: 260 }} option={priceOption} />
      </Card>
      <Card title="基本面" style={{ marginTop: 16 }}>
        <Table dataSource={context?.fundamentals} rowKey={(r: any) => r.period_end_date} pagination={false} columns={[
          { title: '期末', dataIndex: 'period_end_date' },
          { title: '营收', dataIndex: 'revenue' },
          { title: '净利润', dataIndex: 'net_income' },
          { title: 'EPS', dataIndex: 'eps' },
          { title: 'ROE', dataIndex: 'roe' },
          { title: 'PE', dataIndex: 'pe_ttm' },
        ]} />
      </Card>
      <Card title="新闻" style={{ marginTop: 16 }}>
        <Table dataSource={context?.news} rowKey={(r: any) => r.url} pagination={false} columns={[{ title: '标题', dataIndex: 'title' }, { title: '来源', dataIndex: 'source' }, { title: '时间', dataIndex: 'published_at' }]} />
      </Card>
      <Card title="AI 分析" extra={<Button onClick={triggerAnalysis}>请求 AI 分析</Button>} style={{ marginTop: 16 }}>
        <pre>{JSON.stringify(context?.analysis, null, 2) || '暂无'}</pre>
      </Card>
    </div>
  )
}

export default SecurityDetail
