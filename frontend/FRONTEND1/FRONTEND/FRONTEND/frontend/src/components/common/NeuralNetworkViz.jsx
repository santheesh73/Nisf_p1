import React, { useEffect, useRef } from 'react';

const NeuralNetworkViz = () => {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animationFrameId;
    let width, height;

    // Configuration - Matching your reference image (Orange/Purple/White)
    const NODE_COUNT = 150; // Higher density for the brain shape
    const CONNECTION_DISTANCE = 75;
    const ROTATION_SPEED = 0.001; // Very subtle for silhouette focus
    const PULSE_SPEED = 0.025;
    const DATA_PACKET_COUNT = 15;
    
    let nodes = [];
    let packets = [];
    let rotation = 0;
    let pulse = 0;

    const colors = {
      orange: '#f97316',
      purple: '#a855f7',
      white: '#ffffff',
      purpleLine: 'rgba(168, 85, 247, 0.25)'
    };

    class Node {
      constructor(index) {
        this.index = index;
        this.reset();
      }

      reset() {
        // Create side-profile brain shape
        let x, y, z;
        let valid = false;
        
        while (!valid) {
          x = (Math.random() - 0.5) * 320;
          y = (Math.random() - 0.5) * 260;
          z = (Math.random() - 0.5) * 120;
          
          const normX = x / 140;
          const normY = y / 120;
          
          // Improved brain silhouette logic
          const isMain = (normX * normX + normY * normY < 1);
          const isFront = (normX < -0.6 && Math.abs(normY) < 0.5);
          const isBackLower = (normX > 0.4 && normY > 0.4 && Math.pow(normX - 0.6, 2) + Math.pow(normY - 0.6, 2) < 0.3);
          const isStem = (Math.abs(normX - 0.1) < 0.2 && normY > 0.8 && normY < 1.3);

          if ((isMain || isFront || isBackLower || isStem) && !(normY > 1.2)) {
            valid = true;
          }
        }

        this.baseX = x;
        this.baseY = y;
        this.baseZ = z;

        this.x = 0;
        this.y = 0;
        this.z = 0;
        
        // Match the image: Mixture of Orange, White, and subtle Purple
        const rand = Math.random();
        if (rand > 0.8) this.type = 'white';
        else if (rand > 0.1) this.type = 'orange';
        else this.type = 'purple';

        this.size = this.type === 'white' ? Math.random() * 2 + 1.5 : Math.random() * 3 + 1.5;
        this.blinkSpeed = 0.02 + Math.random() * 0.05;
        this.blinkOffset = Math.random() * Math.PI * 2;
      }

      update(rot, p) {
        const cosR = Math.cos(rot);
        const sinR = Math.sin(rot);
        
        const rx = this.baseX * cosR - this.baseZ * sinR;
        const rz = this.baseX * sinR + this.baseZ * cosR;
        
        const floatY = Math.sin(p + this.index * 0.1) * 6;
        
        this.x = rx + width / 2;
        this.y = this.baseY + floatY + height / 2;
        this.z = rz;
        
        this.scale = (rz + 250) / 500;
        this.opacity = 0.3 + (rz + 250) / 500 * 0.7;
      }

      draw(ctx) {
        const s = this.size * this.scale;
        const blink = (Math.sin(Date.now() * this.blinkSpeed + this.blinkOffset) + 1) / 2;
        
        let color;
        switch(this.type) {
          case 'white': color = colors.white; break;
          case 'orange': color = colors.orange; break;
          default: color = colors.purple;
        }

        const opacity = this.opacity * (0.4 + blink * 0.4);
        
        // Faux Glow (Cheaper than shadowBlur)
        ctx.globalAlpha = opacity * 0.3;
        ctx.beginPath();
        ctx.arc(this.x, this.y, s * 2.5, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
        
        ctx.globalAlpha = opacity;
        ctx.beginPath();
        ctx.arc(this.x, this.y, s, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
        
        ctx.globalAlpha = 1.0;
      }
    }

    class DataPacket {
      constructor() {
        this.reset();
      }

      reset() {
        this.startNode = nodes[Math.floor(Math.random() * nodes.length)];
        this.endNode = nodes[Math.floor(Math.random() * nodes.length)];
        
        let dist = this.getDist(this.startNode, this.endNode);
        let attempts = 0;
        while ((dist > CONNECTION_DISTANCE * 1.8 || dist < 30 || this.startNode === this.endNode) && attempts < 25) {
          this.endNode = nodes[Math.floor(Math.random() * nodes.length)];
          dist = this.getDist(this.startNode, this.endNode);
          attempts++;
        }
        
        this.progress = 0;
        this.speed = 0.004 + Math.random() * 0.012;
        this.color = Math.random() > 0.5 ? colors.orange : colors.white;
      }

      getDist(n1, n2) {
        const dx = n1.baseX - n2.baseX;
        const dy = n1.baseY - n2.baseY;
        const dz = n1.baseZ - n2.baseZ;
        return Math.sqrt(dx*dx + dy*dy + dz*dz);
      }

      update() {
        this.progress += this.speed;
        if (this.progress >= 1) this.reset();
      }

      draw(ctx) {
        if (!this.startNode || !this.endNode) return;
        
        const x = this.startNode.x + (this.endNode.x - this.startNode.x) * this.progress;
        const y = this.startNode.y + (this.endNode.y - this.startNode.y) * this.progress;
        const scale = this.startNode.scale + (this.endNode.scale - this.startNode.scale) * this.progress;
        
        ctx.globalAlpha = 0.8;
        ctx.beginPath();
        ctx.arc(x, y, 2 * scale, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.globalAlpha = 1.0;
      }
    }

    const init = () => {
      nodes = [];
      for (let i = 0; i < NODE_COUNT; i++) nodes.push(new Node(i));
      packets = [];
      for (let i = 0; i < DATA_PACKET_COUNT; i++) packets.push(new DataPacket());
    };

    const handleResize = () => {
      if (!canvas.parentElement) return;
      width = canvas.width = canvas.parentElement.offsetWidth;
      height = canvas.height = canvas.parentElement.offsetHeight;
      init();
    };

    window.addEventListener('resize', handleResize);
    handleResize();

    const animate = () => {
      ctx.clearRect(0, 0, width, height);
      
      rotation += ROTATION_SPEED;
      pulse += PULSE_SPEED;

      nodes.forEach(node => node.update(rotation, pulse));

      // Draw Connections (Dense Purple Mesh)
      ctx.lineWidth = 1.4;
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const n1 = nodes[i];
          const n2 = nodes[j];
          const dx = n1.x - n2.x;
          const dy = n1.y - n2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < CONNECTION_DISTANCE * n1.scale) {
            const opacity = (1 - dist / (CONNECTION_DISTANCE * n1.scale)) * 0.6 * n1.opacity;
            ctx.strokeStyle = `rgba(168, 85, 247, ${opacity})`;
            ctx.beginPath();
            ctx.moveTo(n1.x, n1.y);
            ctx.lineTo(n2.x, n2.y);
            ctx.stroke();
          }
        }
      }

      nodes.forEach(node => node.draw(ctx));
      packets.forEach(packet => {
        packet.update();
        packet.draw(ctx);
      });

      animationFrameId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <div ref={containerRef} className="relative h-full w-full overflow-hidden">
      <canvas 
        ref={canvasRef} 
        className="block h-full w-full"
      />
    </div>
  );
};

export default NeuralNetworkViz;
