export default function StatCard({label,value}){return <article className="card"><small>{label}</small><strong>{value??'—'}</strong></article>}
