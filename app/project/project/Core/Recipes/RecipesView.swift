//
//  RecipesView.swift
//  project
//
//  Created by Drew S on 3/6/24.
//

import SwiftUI

struct RecipesView: View {
    let boxGrey = Color(hex: 0x404040)
    let textGrey = Color(hex: 0x999999)

    var body: some View {
        VStack{
            VStack
            {
                HStack{
                    Text("Recipes")
                        .foregroundColor(textGrey)
                        .font(.system(size:40))
                        .padding(.horizontal, 30)
                    Spacer()
                }
                
            }.background(Color.black)
            Spacer()
        }.background(Color.black)
    }
}

#Preview {
    RecipesView()
}
