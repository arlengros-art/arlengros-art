import React from 'react';

interface ImageCardProps {
  src: string;
  alt?: string;
}

const ImageCard: React.FC<ImageCardProps> = ({ src, alt }) => (
  <div className="image-card">
    <img src={src} alt={alt || 'generated'} />
  </div>
);

export default ImageCard;
