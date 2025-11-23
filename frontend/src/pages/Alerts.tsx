import { useEffect, useState } from 'react'
import { Card, List } from 'antd'
import api from '../api'

const Alerts: React.FC = () => {
  const [alerts, setAlerts] = useState<any[]>([])

  useEffect(() => {
    api.get('/api/alerts').then(res => setAlerts(res.data))
  }, [])

  return (
    <Card title="提醒列表">
      <List dataSource={alerts} renderItem={item => (
        <List.Item>
          <div>{item.message}</div>
          <div>{item.triggered_at}</div>
        </List.Item>
      )} />
    </Card>
  )
}

export default Alerts
