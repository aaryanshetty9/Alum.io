"use client"

import type React from "react"
import { useEffect, useRef } from "react"

const SpaceBackground: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    class Star {
      x: number
      y: number
      z: number
      xPrev: number
      yPrev: number

      constructor() {
        this.x = Math.random() * canvas.width - canvas.width / 2
        this.y = Math.random() * canvas.height - canvas.height / 2
        this.z = Math.random() * canvas.width
        this.xPrev = this.x
        this.yPrev = this.y
      }

      update(speed: number) {
        this.xPrev = this.x
        this.yPrev = this.y
        this.z -= speed
        if (this.z <= 0) {
          this.z = canvas.width
          this.x = Math.random() * canvas.width - canvas.width / 2
          this.y = Math.random() * canvas.height - canvas.height / 2
          this.xPrev = this.x
          this.yPrev = this.y
        }
      }

      draw() {
        const x = (this.x / this.z) * canvas.width + canvas.width / 2
        const y = (this.y / this.z) * canvas.height + canvas.height / 2
        const xPrev = (this.xPrev / this.z) * canvas.width + canvas.width / 2
        const yPrev = (this.yPrev / this.z) * canvas.height + canvas.height / 2

        ctx!.beginPath()
        ctx!.moveTo(xPrev, yPrev)
        ctx!.lineTo(x, y)
        ctx!.stroke()
      }
    }

    const stars = Array.from({ length: 1000 }, () => new Star())

    const animate = () => {
      ctx.fillStyle = "rgba(0, 0, 0, 0.2)"
      ctx.fillRect(0, 0, canvas.width, canvas.height)
      ctx.strokeStyle = "white"
      ctx.lineWidth = 0.5

      stars.forEach((star) => {
        star.update(2)
        star.draw()
      })

      requestAnimationFrame(animate)
    }

    animate()

    const handleResize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }

    window.addEventListener("resize", handleResize)

    return () => {
      window.removeEventListener("resize", handleResize)
    }
  }, [])

  return <canvas ref={canvasRef} className="fixed top-0 left-0 w-full h-full" />
}

export default SpaceBackground

