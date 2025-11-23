import { Card, Col, Row, Statistic, List } from 'antd'
import ReactECharts from 'echarts-for-react'
import { useEffect, useState } from 'react'
import api from '../api'
import { useNavigate } from 'react-router-dom'

const Dashboard: React.FC = () => {
  const [summary, setSummary] = useState<any>(null)
  const [alerts, setAlerts] = useState<any[]>([])
  const [equityCurve, setEquityCurve] = useState<any[]>([])
  const navigate = useNavigate()

  useEffect(() => {
    api.get('/api/portfolio/summary').then(res => setSummary(res.data))
    api.get('/api/alerts').then(res => setAlerts(res.data))
    api.get('/api/portfolio/equity_curve').then(res => setEquityCurve(res.data))
  }, [])

  const option = {
    xAxis: { type: 'category', data: equityCurve.map(p => p.date) },
    yAxis: { type: 'value' },
    series: [{ data: equityCurve.map(p => p.equity), type: 'line' }]
  }

  return (
    <div>
      <Row gutter={16}>
        <Col span={6}><Card><Statistic title="总资产" value={summary?.equity ?? 0} precision={2} /></Card></Col>
        <Col span={6}><Card><Statistic title="总盈亏" value={summary?.pnl ?? 0} precision={2} /></Card></Col>
        <Col span={6}><Card><Statistic title="今日变化" value={summary?.today_change ?? 0} precision={2} /></Card></Col>
        <Col span={6}><Card><Statistic title="今年收益率" value={(summary?.ytd_return ?? 0) * 100} suffix="%" precision={2} /></Card></Col>
      </Row>
      <Card title="净值曲线" style={{ marginTop: 16 }}>
        <ReactECharts style={{ height: 300 }} option={option} />
      </Card>
      <Card title="提醒" style={{ marginTop: 16 }}>
        <List dataSource={alerts} renderItem={item => (
          <List.Item onClick={() => navigate('/alerts')} style={{ cursor: 'pointer' }}>
            {item.message}
          </List.Item>
        )} />
      </Card>
    </div>
  )
}

export default Dashboard
