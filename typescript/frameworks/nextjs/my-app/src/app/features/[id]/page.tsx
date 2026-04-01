export const dynamicParams = false

export async function generateStaticParams() {
  return [
    { id: '1' },
    { id: '2' },
  ]
  //adicionar fallback
}

export default async function Produto({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params

  return <h1>dynamic routing: {id}</h1>
}