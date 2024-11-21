#include <stdint.h>
#include <stdio.h>

#define ROTL8(x,shift) ((uint8_t) ((x) << (shift)) | ((x) >> (8 - (shift))))

void initialize_aes_sbox(uint8_t sbox[256]) {
	uint8_t p = 1, q = 1;
	
	/* loop invariant: p * q == 1 in the Galois field */
	do {
		/* multiply p by 3 */ //$$S=s_7x^7+s_6x^6+s_5x^5+s_4x^4+s_3x^3+s_2x^2+s_1x+s_0$$;  $$X2=\{02\}*S=x*S=s_7x^8+s_6x^7+s_5x^6+s_4x^5+s_3x^4+s_2x^3+s_1x^2+s_0x \; mod \; p(x) =s_6x^7+s_5x^6+s_4x^5+(s_3+s_7)x^4+(s_2+s_7)x^3+s_1x^2+(s_0+s_7)x+s_7$$
		p = p ^ (p << 1) ^ (p & 0x80 ? 0x1B : 0);

		/* divide q by 3 (equals multiplication by 0xf6) */
		q ^= q << 1;
		q ^= q << 2;
		q ^= q << 4;
		q ^= q & 0x80 ? 0x09 : 0;

		/* compute the affine transformation */
		uint8_t xformed = q ^ ROTL8(q, 1) ^ ROTL8(q, 2) ^ ROTL8(q, 3) ^ ROTL8(q, 4);

		sbox[p] = xformed ^ 0x63;
	} while (p != 1);

	/* 0 is a special case since it has no inverse */
	sbox[0] = 0x63;
}

int main() {
    uint8_t sbox[256];
    initialize_aes_sbox(sbox);

    for (int i = 0; i < 256; i++) {
        printf("0x%02x ", sbox[i]);
        if ((i + 1) % 16 == 0) {
            printf("\n");
        }
    }

    return 0;
}
