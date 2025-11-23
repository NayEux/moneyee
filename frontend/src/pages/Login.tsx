import { Button, Card, Form, Input, message } from 'antd'
import api from '../api'

interface Props {
  onLogin: (token: string) => void
}

const Login: React.FC<Props> = ({ onLogin }) => {
  const onFinish = async (values: any) => {
    try {
      const res = await api.post('/api/auth/login', new URLSearchParams({
        username: values.email,
        password: values.password
      }))
      localStorage.setItem('token', res.data.access_token)
      onLogin(res.data.access_token)
    } catch (e) {
      message.error('登录失败')
    }
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', marginTop: 100 }}>
      <Card title="登录">
        <Form layout="vertical" onFinish={onFinish} style={{ width: 320 }}>
          <Form.Item name="email" label="邮箱" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="password" label="密码" rules={[{ required: true }]}>
            <Input.Password />
          </Form.Item>
          <Button type="primary" htmlType="submit" block>登录</Button>
        </Form>
      </Card>
    </div>
  )
}

export default Login
