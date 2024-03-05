//
//  ContentView.swift
//  project
//
//  Created by Drew S on 2/27/24.
//

import SwiftUI

struct ContentView: View {
    @State private var showDetails = false
    var body: some View {
        VStack {
            Image(systemName: "globe")
                .imageScale(.large)
                .foregroundStyle(.tint)
            Text("Hello, world!")
            
            Button("Show details") {
                            showDetails.toggle()
                        }

            if showDetails {
                Text("update")
                .font(.title)}
        }
    }
}

#Preview {
    ContentView()
}
