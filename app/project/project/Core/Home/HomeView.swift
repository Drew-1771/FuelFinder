//
//  HomeView.swift
//  project
//
//  Created by Drew S on 3/5/24.
//

import SwiftUI

extension Color {
    init(hex: UInt32) {
        let red = Double((hex & 0xFF0000) >> 16) / 255.0
        let green = Double((hex & 0x00FF00) >> 8) / 255.0
        let blue = Double(hex & 0x0000FF) / 255.0
        self.init(red: red, green: green, blue: blue)
    }
}

struct HomeView: View {
    
    
    let customColor = Color(hex: 0x474747)
    var body: some View {
        HStack {
            VStack(spacing: 20){
                PreviewBox(color: customColor, description: "one")
                PreviewBox(color: customColor, description:  "two")
                PreviewBox(color: customColor, description: "three")
                Spacer()
            }.padding(.horizontal, 2)

            VStack(spacing: 20){
                PreviewBox(color: customColor, description:  "four")
                PreviewBox(color: customColor, description:  "five")
                PreviewBox(color: customColor, description:  "six")
                Spacer()
            }.padding(.horizontal, 2)

        }
            .padding(.horizontal, 20)
            .padding(.bottom, 20)
            .background(Color.black)
    }
}

struct PreviewBox: View {
    var color: Color
    var description: String
    
    var body: some View {
        Button(action: {
            print("selected preview: \(description)")
        }) {
            HStack {
                Image(systemName: "photo.on.rectangle")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 30, height: 30)
                    .padding()
                    .foregroundColor(.white)
                Text(description)
                    .foregroundColor(.white)
                    .padding()
                Spacer()
            }
            .background(color)
            .cornerRadius(10)
        }
    }
}

#Preview {
    HomeView()
}
