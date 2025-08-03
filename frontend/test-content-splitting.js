#!/usr/bin/env node

// Test script to verify content splitting logic
function splitContentForPages(content, maxLength = 4000) {
  if (!content || content.length <= maxLength) return [content || 'No content available'];
  
  const chunks = [];
  let currentChunk = '';
  
  // Split by sentences first, preserving punctuation and spacing
  const sentences = content.match(/[^.!?]*[.!?]*\s*/g) || [content];
  
  for (const sentence of sentences) {
    if (!sentence.trim()) continue; // Skip empty sentences
    
    // If adding this sentence would exceed the limit and we have content
    if ((currentChunk + sentence).length > maxLength && currentChunk.length > 0) {
      chunks.push(currentChunk.trim());
      currentChunk = sentence;
    } else {
      currentChunk += sentence;
    }
  }
  
  // Always add the remaining content
  if (currentChunk.trim()) {
    chunks.push(currentChunk.trim());
  }
  
  // Ensure we return at least one chunk with content
  if (chunks.length === 0) {
    chunks.push(content);
  }
  
  return chunks;
}

// Test with sample content
const testContent = `
## Visual Layout Analysis

Grid alignment and spacing consistency: The layout appears to have a consistent grid system, with well-defined spacing between elements.

Visual hierarchy and information architecture: The information is organized in a clear and structured manner, with a clear hierarchy of information.

White space utilization: The use of white space is effective in creating a clean and uncluttered look.

Specific layout improvements: None required at this time.

## Responsiveness & UX

Mobile-first design indicators: The design appears to be responsive, with elements adapting well to different screen sizes.

Navigation clarity and usability: The navigation is clear and easy to use, with intuitive structure and clear labels.

Call-to-action effectiveness: The call-to-action buttons are prominent and clearly visible, making it easy for users to take action.

User experience flow assessment: The overall user experience is smooth and intuitive, with a logical flow of information.
`;

console.log('Original content length:', testContent.length);
console.log('Content:', testContent);
console.log('\n--- Splitting content ---\n');

const chunks = splitContentForPages(testContent, 400); // Use smaller limit for testing
console.log('Number of chunks:', chunks.length);

chunks.forEach((chunk, index) => {
  console.log(`\n--- Chunk ${index + 1} (${chunk.length} chars) ---`);
  console.log(chunk);
});

// Test original total length vs combined chunks length
const totalChunkLength = chunks.join('').length;
console.log(`\nOriginal length: ${testContent.length}`);
console.log(`Combined chunks length: ${totalChunkLength}`);
console.log(`Content preserved: ${testContent.length === totalChunkLength ? 'YES' : 'NO'}`);
