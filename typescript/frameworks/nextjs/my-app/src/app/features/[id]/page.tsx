export default async function Produto({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params

  return <h1>dynamic routing: {id}</h1>
}