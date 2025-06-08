export default function TransactionCard({ tx }) {
    return (
      <div className="card">
        <p><strong>Bank:</strong> {tx.bank_name}</p>
        <p><strong>Amount:</strong> ₹{tx.amount}</p>
        <p><strong>Type:</strong> {tx.transaction_type}</p>
        {/* <p><strong>Confidence:</strong> {tx.confidence}%</p> */}
        <p><strong>Time:</strong> {new Date(tx.created_at).toLocaleString()}</p>
      </div>
    );
  }
  