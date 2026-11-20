import React from "react";
import {
  Body,
  Button,
  Column,
  Container,
  Head,
  Heading,
  Hr,
  Html,
  Img,
  Preview,
  Row,
  Section,
  Text,
} from "react-email";

const navy = "#1e3a8a";
const muted = "#64748b";
const pageBg = "#f0f4f8";

const formatCrc = (amount) => {
  const value = Number(amount) || 0;
  return `CRC ${value.toLocaleString("es-CR")}`;
};

const InfoRow = ({ label, value }) => {
  if (!value) {
    return null;
  }

  return (
    <Row>
      <Column style={{ width: "140px", padding: "6px 0", verticalAlign: "top" }}>
        <Text style={styles.infoLabel}>{label}</Text>
      </Column>
      <Column style={{ padding: "6px 0" }}>
        <Text style={styles.infoValue}>{value}</Text>
      </Column>
    </Row>
  );
};

export const OrderConfirmedEmail = ({
  fullName = "cliente",
  username,
  email,
  phone,
  address,
  payment = "Sinpe",
  orderNumber = "",
  total = 0,
  catalogUrl = "http://localhost:5173/products",
  items = [],
}) => (
  <Html lang="es">
    <Head />
    <Preview>{`PawStore — Pedido ${orderNumber} confirmado`}</Preview>
    <Body style={styles.body}>
      <Container style={styles.container}>
        <Section style={styles.header}>
          <Text style={styles.brand}>PawStore</Text>
        </Section>

        <Section style={styles.hero}>
          <Text style={styles.check}>✓</Text>
          <Heading style={styles.title}>¡Gracias por tu compra!</Heading>
          <Text style={styles.message}>
            Hola {fullName}, hemos recibido tu pedido #{orderNumber} y ya lo
            estamos procesando.
          </Text>
        </Section>

        <Section style={styles.block}>
          <Heading as="h2" style={styles.subtitle}>
            Datos del cliente
          </Heading>
          <Section style={styles.card}>
            <InfoRow label="Nombre" value={fullName} />
            <InfoRow label="Usuario" value={username} />
            <InfoRow label="Correo" value={email} />
            <InfoRow label="Teléfono" value={phone} />
            <InfoRow label="Dirección" value={address} />
            <InfoRow label="Pago" value={payment} />
          </Section>
        </Section>

        <Section style={styles.block}>
          <Heading as="h2" style={styles.subtitle}>
            Resumen del pedido
          </Heading>
          {items.length === 0 ? (
            <Text style={styles.message}>No hay productos en este pedido.</Text>
          ) : (
            items.map((item) => (
              <Section key={`${item.name}-${item.quantity}`} style={styles.item}>
                <Row>
                  <Column style={{ width: "58px" }}>
                    {item.imageUrl ? (
                      <Img
                        src={item.imageUrl}
                        alt={item.name}
                        width="50"
                        height="50"
                        style={styles.itemImage}
                      />
                    ) : null}
                  </Column>
                  <Column>
                    <Text style={styles.itemName}>{item.name}</Text>
                    <Text style={styles.itemQty}>Cantidad: {item.quantity}</Text>
                  </Column>
                  <Column align="right" style={{ width: "110px" }}>
                    <Text style={styles.itemPrice}>
                      {formatCrc(item.lineTotal)}
                    </Text>
                  </Column>
                </Row>
              </Section>
            ))
          )}
        </Section>

        <Section style={styles.totalWrap}>
          <Section style={styles.totalBox}>
            <Row>
              <Column style={{ width: "50%" }}>
                <Text style={styles.totalLabel}>Total pagado</Text>
              </Column>
              <Column align="right" style={{ width: "50%" }}>
                <Text style={styles.totalValue}>{formatCrc(total)}</Text>
              </Column>
            </Row>
          </Section>
        </Section>

        <Hr style={styles.hr} />

        <Section style={{ textAlign: "center", paddingBottom: "32px" }}>
          <Button href={catalogUrl} style={styles.button}>
            Volver al catálogo
          </Button>
        </Section>
      </Container>
    </Body>
  </Html>
);

OrderConfirmedEmail.PreviewProps = {
  fullName: "Ana Pérez",
  username: "ana",
  email: "ana@example.com",
  phone: "8888-8888",
  address: "San José, Costa Rica",
  payment: "Sinpe",
  orderNumber: "PW-1001",
  total: 25000,
  catalogUrl: "http://localhost:5173/products",
  items: [
    {
      name: "Alimento para perro",
      quantity: 2,
      imageUrl: "",
      lineTotal: 25000,
    },
  ],
};

export default OrderConfirmedEmail;

const styles = {
  body: {
    backgroundColor: pageBg,
    fontFamily: "Arial, Helvetica, sans-serif",
    margin: 0,
    padding: "32px 12px",
  },
  container: {
    backgroundColor: "#ffffff",
    borderRadius: "12px",
    maxWidth: "600px",
    width: "100%",
  },
  header: {
    backgroundColor: navy,
    padding: "20px 28px",
  },
  brand: {
    color: "#ffffff",
    fontSize: "20px",
    fontWeight: "bold",
    margin: 0,
  },
  hero: {
    textAlign: "center",
    padding: "32px 24px 8px 24px",
  },
  check: {
    backgroundColor: "#ecfdf3",
    borderRadius: "36px",
    color: "#27ae60",
    display: "inline-block",
    fontSize: "32px",
    height: "64px",
    lineHeight: "64px",
    margin: "0 auto 12px auto",
    textAlign: "center",
    width: "64px",
  },
  title: {
    color: navy,
    fontSize: "24px",
    fontWeight: 600,
    margin: "0 0 12px 0",
  },
  message: {
    color: "#666666",
    fontSize: "16px",
    lineHeight: "1.5",
    margin: 0,
  },
  block: {
    padding: "16px 28px",
  },
  subtitle: {
    color: "#444444",
    fontSize: "18px",
    margin: "0 0 12px 0",
  },
  card: {
    backgroundColor: "#f8fafc",
    border: "1px solid #e2e8f0",
    borderRadius: "8px",
    padding: "8px 16px",
  },
  infoLabel: {
    color: muted,
    fontSize: "13px",
    margin: 0,
  },
  infoValue: {
    color: "#0f172a",
    fontSize: "15px",
    fontWeight: 600,
    margin: 0,
  },
  item: {
    border: "1px solid #eeeeee",
    borderRadius: "8px",
    marginBottom: "8px",
    padding: "12px",
  },
  itemImage: {
    border: "1px solid #dddddd",
    borderRadius: "4px",
    objectFit: "cover",
  },
  itemName: {
    color: "#333333",
    fontSize: "16px",
    fontWeight: 600,
    margin: "0 0 4px 0",
  },
  itemQty: {
    color: "#666666",
    fontSize: "14px",
    margin: 0,
  },
  itemPrice: {
    color: navy,
    fontSize: "16px",
    fontWeight: "bold",
    margin: 0,
  },
  totalWrap: {
    padding: "8px 28px 16px 28px",
  },
  totalBox: {
    backgroundColor: "#f8fafc",
    borderRadius: "8px",
    padding: "12px 16px",
  },
  totalLabel: {
    color: "#4b5563",
    fontSize: "16px",
    fontWeight: 600,
    margin: 0,
  },
  totalValue: {
    color: navy,
    fontSize: "18px",
    fontWeight: 700,
    margin: 0,
    whiteSpace: "nowrap",
  },
  hr: {
    borderColor: "#e5e7eb",
    margin: "8px 0 24px 0",
  },
  button: {
    backgroundColor: navy,
    borderRadius: "20px",
    color: "#ffffff",
    display: "inline-block",
    fontSize: "16px",
    fontWeight: 600,
    padding: "12px 24px",
    textDecoration: "none",
  },
};
