import { useEffect, useState } from 'react'
import { Card, Form, Input, Button, Select } from 'antd'
import api from '../api'

const Preferences: React.FC = () => {
  const [form] = Form.useForm()

  useEffect(() => {
    api.get('/api/preferences').then(res => {
      form.setFieldsValue(res.data)
    })
  }, [])

  const onFinish = async (values: any) => {
    await api.put('/api/preferences', values)
  }

  return (
    <Card title="偏好设置">
      <Form form={form} layout="vertical" onFinish={onFinish} initialValues={{ risk_level: 'balanced' }}>
        <Form.Item label="风险等级" name="risk_level">
          <Select options={[{ value: 'conservative' }, { value: 'balanced' }, { value: 'aggressive' }]} />
        </Form.Item>
        <Form.Item label="持仓周期(天)" name="preferred_holding_period_days">
          <Input type="number" />
        </Form.Item>
        <Form.Item label="偏好行业" name="preferred_sectors">
          <Input placeholder="逗号分隔" />
        </Form.Item>
        <Form.Item label="回避行业" name="avoided_sectors">
          <Input placeholder="逗号分隔" />
        </Form.Item>
        <Button type="primary" htmlType="submit">保存</Button>
      </Form>
    </Card>
  )
}

export default Preferences
