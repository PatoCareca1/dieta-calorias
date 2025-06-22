// frontend/src/pages/CalculadoraPage.tsx
import React, { useState } from 'react';
import { Container, Form, Button, Row, Col, Card, Spinner, Alert } from 'react-bootstrap';
import api from '../services/api';

// Interface para os dados do formulário, espelhando o schema Pydantic `DadosUsuario`
interface DadosUsuario {
  peso: number;
  altura: number;
  idade: number;
  sexo: 'masculino' | 'feminino';
  nivel_atividade: 'sedentario' | 'leve' | 'moderado' | 'ativo' | 'muito_ativo';
  objetivo: 'perder_gordura' | 'manter_peso' | 'ganhar_massa';
}

// Interface para a resposta da API, espelhando `MetasNutricionais`
interface MetasNutricionais {
    calorias_diarias: number;
    proteinas_diarias: number;
    carboidratos_diarios: number;
    gorduras_diarias: number;
}

const CalculadoraPage: React.FC = () => {
  const [formData, setFormData] = useState<DadosUsuario>({
    peso: 70, altura: 175, idade: 25, sexo: 'masculino',
    nivel_atividade: 'sedentario', objetivo: 'manter_peso',
  });
  const [metas, setMetas] = useState<MetasNutricionais | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMetas(null);
    try {
      const response = await api.post<MetasNutricionais>('/calcular-calorias/', formData);
      setMetas(response.data);
    } catch (err) {
      setError('Não foi possível calcular as metas. Verifique os dados e tente novamente.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="mt-5">
      <Row>
        <Col md={{ span: 6, offset: 3 }}>
          <Card>
            <Card.Body>
              <Card.Title as="h2" className="text-center mb-4">Calculadora de Metas Nutricionais</Card.Title>
              <Form onSubmit={handleSubmit}>
                {/* Campos do formulário (Peso, Altura, Idade) */}
                <Form.Group className="mb-3">
                  <Form.Label>Peso (kg)</Form.Label>
                  <Form.Control type="number" name="peso" value={formData.peso} onChange={handleChange} required />
                </Form.Group>
                {/* ... adicione os campos para altura e idade da mesma forma ... */}

                {/* Sexo */}
                <Form.Group className="mb-3">
                    <Form.Label>Sexo</Form.Label>
                    <Form.Select name="sexo" value={formData.sexo} onChange={handleChange}>
                        <option value="masculino">Masculino</option>
                        <option value="feminino">Feminino</option>
                    </Form.Select>
                </Form.Group>

                {/* Nível de Atividade */}
                <Form.Group className="mb-3">
                    <Form.Label>Nível de Atividade Física</Form.Label>
                    <Form.Select name="nivel_atividade" value={formData.nivel_atividade} onChange={handleChange}>
                        <option value="sedentario">Sedentário (pouco ou nenhum exercício)</option>
                        <option value="leve">Leve (exercício leve 1-3 dias/semana)</option>
                        <option value="moderado">Moderado (exercício moderado 3-5 dias/semana)</option>
                        <option value="ativo">Ativo (exercício pesado 6-7 dias/semana)</option>
                        <option value="muito_ativo">Muito Ativo (exercício pesado diário e trabalho físico)</option>
                    </Form.Select>
                </Form.Group>

                {/* Objetivo */}
                <Form.Group className="mb-3">
                    <Form.Label>Qual seu objetivo?</Form.Label>
                    <Form.Select name="objetivo" value={formData.objetivo} onChange={handleChange}>
                        <option value="perder_gordura">Perder Gordura</option>
                        <option value="manter_peso">Manter o Peso (Normocalórica)</option>
                        <option value="ganhar_massa">Ganhar Massa Muscular</option>
                    </Form.Select>
                </Form.Group>

                <div className="d-grid">
                  <Button variant="primary" type="submit" disabled={loading}>
                    {loading ? <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" /> : 'Calcular'}
                  </Button>
                </div>
              </Form>
            </Card.Body>
          </Card>

          {error && <Alert variant="danger" className="mt-4">{error}</Alert>}

          {metas && (
            <Card className="mt-4 text-center">
                <Card.Header as="h3">Suas Metas Diárias</Card.Header>
                <Card.Body>
                    <Card.Title>{Math.round(metas.calorias_diarias)} kcal</Card.Title>
                    <Row>
                        <Col><strong>Proteínas:</strong> {Math.round(metas.proteinas_diarias)}g</Col>
                        <Col><strong>Carboidratos:</strong> {Math.round(metas.carboidratos_diarios)}g</Col>
                        <Col><strong>Gorduras:</strong> {Math.round(metas.gorduras_diarias)}g</Col>
                    </Row>
                </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default CalculadoraPage;