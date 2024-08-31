import { NextResponse } from 'next/server'
import OpenAI from 'openai'
import { ChatCompletionMessageParam } from 'openai/resources/chat'

// API anahtarının varlığını kontrol eden fonksiyon
function checkApiKey() {
  if (!process.env.OPENAI_API_KEY) {
    throw new Error('OpenAI API anahtarı bulunamadı. Lütfen .env dosyanızı kontrol edin ve OPENAI_API_KEY değerini ayarlayın.')
  }
}

export async function POST(req: Request) {
  try {
    // API anahtarını kontrol et
    checkApiKey()

    const { messages } = await req.json()

    const openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    })

    const chatCompletion = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: messages as ChatCompletionMessageParam[],
    })

    const reply = chatCompletion.choices[0].message

    return NextResponse.json(reply)
  } catch (error: any) {
    console.error('Hata:', error.message)
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}