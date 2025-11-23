import { Card, Table, Button, Row, Col } from 'antd'
import ReactECharts from 'echarts-for-react'
import { useEffect, useState } from 'react'
import api from '../api'
import { useNavigate } from 'react-router-dom'

const Portfolio: React.FC = () => {
  const [positions, setPositions] = useState<any[]>([])
  const [breakdown, setBreakdown] = useState<any[]>([])
  const navigate = useNavigate()

  useEffect(() => {
    api.get('/api/portfolio/positions').then(res => setPositions(res.data))
    api.get('/api/portfolio/holdings_breakdown').then(res => setBreakdown(res.data))
  }, [])

  const chartOption = {
    series: [{
      type: 'pie',
      data: breakdown.map(b => ({ value: b.weight, name: b.label }))
    }]
  }

  const columns = [
    { title: '代码', dataIndex: 'symbol' },
    { title: '市场', dataIndex: 'market' },
    { title: '名称', dataIndex: 'name' },
    { title: '数量', dataIndex: 'quantity' },
    { title: '均价', dataIndex: 'avg_cost' },
    { title: '现价', dataIndex: 'last_price' },
    { title: '市值', dataIndex: 'market_value' },
    { title: '浮盈亏', dataIndex: 'unrealized_pnl' },
    { title: '仓位', dataIndex: 'weight', render: (v: number) => `${(v * 100).toFixed(2)}%` },
    { title: '操作', render: (_: any, record: any) => <Button type="link" onClick={() => navigate(`/security/${record.symbol}`)}>详情</Button> }
  ]

  return (
    <Row gutter={16}>
      <Col span={16}>
        <Card title="当前持仓">
          <Table columns={columns} dataSource={positions} rowKey="symbol" pagination={false} />
        </Card>
      </Col>
      <Col span={8}>
        <Card title="行业/市场分布">
          <ReactECharts style={{ height: 300 }} option={chartOption} />
        </Card>
      </Col>
    </Row>
  )
}

export default Portfolio
